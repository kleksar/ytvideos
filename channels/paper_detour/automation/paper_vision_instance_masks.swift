#!/usr/bin/env swift
import CoreVideo
import Foundation
import ImageIO
import Vision

struct MaskExportError: Error, CustomStringConvertible {
    let description: String
}

guard CommandLine.arguments.count == 3 else {
    fatalError("Usage: swift paper_vision_instance_masks.swift <master.png> <output-directory>")
}

let inputURL = URL(fileURLWithPath: CommandLine.arguments[1]).standardizedFileURL
let outputDirectory = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true).standardizedFileURL
guard FileManager.default.fileExists(atPath: inputURL.path) else {
    fatalError("Master image not found: \(inputURL.path)")
}
try FileManager.default.createDirectory(at: outputDirectory, withIntermediateDirectories: true)

guard let imageSource = CGImageSourceCreateWithURL(inputURL as CFURL, nil),
      let sourceImage = CGImageSourceCreateImageAtIndex(imageSource, 0, nil) else {
    fatalError("Could not decode master image: \(inputURL.path)")
}
let sourceWidth = sourceImage.width
let sourceHeight = sourceImage.height

let handler = VNImageRequestHandler(url: inputURL, options: [:])
let request = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])

guard let observation = request.results?.first else {
    throw MaskExportError(description: "Vision detected no foreground instances")
}
guard !observation.allInstances.isEmpty else {
    throw MaskExportError(description: "Vision returned an empty instance set")
}

print("Master: \(sourceWidth)x\(sourceHeight)")
print("Detected instances: \(observation.allInstances)")

for instanceID in observation.allInstances {
    let pixelBuffer = try observation.generateScaledMaskForImage(
        forInstances: IndexSet(integer: instanceID),
        from: handler
    )

    let width = CVPixelBufferGetWidth(pixelBuffer)
    let height = CVPixelBufferGetHeight(pixelBuffer)
    let bytesPerRow = CVPixelBufferGetBytesPerRow(pixelBuffer)
    let pixelFormat = CVPixelBufferGetPixelFormatType(pixelBuffer)
    guard width == sourceWidth, height == sourceHeight else {
        throw MaskExportError(
            description: "Instance \(instanceID) mask is \(width)x\(height); expected \(sourceWidth)x\(sourceHeight)"
        )
    }
    guard pixelFormat == kCVPixelFormatType_OneComponent32Float || pixelFormat == kCVPixelFormatType_OneComponent8 else {
        throw MaskExportError(description: "Unsupported Vision mask pixel format: \(pixelFormat)")
    }

    CVPixelBufferLockBaseAddress(pixelBuffer, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(pixelBuffer, .readOnly) }
    guard let baseAddress = CVPixelBufferGetBaseAddress(pixelBuffer) else {
        throw MaskExportError(description: "Mask \(instanceID) has no base address")
    }

    var grayscale = [UInt8](repeating: 0, count: width * height)
    for y in 0..<height {
        let row = baseAddress.advanced(by: y * bytesPerRow)
        if pixelFormat == kCVPixelFormatType_OneComponent32Float {
            let values = row.assumingMemoryBound(to: Float32.self)
            for x in 0..<width {
                let raw = values[x]
                let value = raw.isFinite ? min(1, max(0, raw)) : 0
                grayscale[y * width + x] = UInt8((value * 255).rounded())
            }
        } else {
            let values = row.assumingMemoryBound(to: UInt8.self)
            for x in 0..<width {
                grayscale[y * width + x] = values[x]
            }
        }
    }

    var pgm = Data("P5\n\(width) \(height)\n255\n".utf8)
    pgm.append(contentsOf: grayscale)
    let outputURL = outputDirectory.appendingPathComponent("instance_\(instanceID).pgm")
    try pgm.write(to: outputURL, options: .atomic)
    print("Saved \(outputURL.path) (\(width)x\(height))")
}
