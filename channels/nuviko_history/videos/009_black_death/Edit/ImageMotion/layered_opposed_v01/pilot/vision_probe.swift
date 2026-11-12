import Foundation
import Vision
import ImageIO
import CoreImage
import CoreVideo

let args = CommandLine.arguments
if args.count != 3 { fatalError("usage: vision_probe.swift IMAGE OUTDIR") }
let imageURL = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2], isDirectory: true)
try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
let handler = VNImageRequestHandler(url: imageURL, options: [:])
let request = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([request])
guard let observation = request.results?.first else { fatalError("No instance mask") }
let ctx = CIContext(options: nil)
var report: [[String: Any]] = []
for instance in observation.allInstances {
    let mask = try observation.generateScaledMaskForImage(forInstances: IndexSet(integer: instance), from: handler)
    let w = CVPixelBufferGetWidth(mask), h = CVPixelBufferGetHeight(mask)
    CVPixelBufferLockBaseAddress(mask, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(mask, .readOnly) }
    let base = CVPixelBufferGetBaseAddress(mask)!.assumingMemoryBound(to: UInt8.self)
    let rowBytes = CVPixelBufferGetBytesPerRow(mask)
    var count = 0, minX = w, minY = h, maxX = -1, maxY = -1
    for y in 0..<h { for x in 0..<w where base[y*rowBytes+x] > 16 {
        count += 1; minX = min(minX,x); maxX = max(maxX,x); minY = min(minY,y); maxY = max(maxY,y)
    }}
    let ci = CIImage(cvPixelBuffer: mask)
    guard let cg = ctx.createCGImage(ci, from: ci.extent) else { fatalError("Could not create CGImage") }
    let path = outDir.appendingPathComponent(String(format: "mask_%02d.png", instance))
    guard let dest = CGImageDestinationCreateWithURL(path as CFURL, "public.png" as CFString, 1, nil) else { fatalError("No image destination") }
    CGImageDestinationAddImage(dest, cg, nil); CGImageDestinationFinalize(dest)
    report.append(["instance": instance, "width": w, "height": h, "count": count, "bbox": [minX,minY,maxX,maxY]])
}
let data = try JSONSerialization.data(withJSONObject: report, options: [.prettyPrinted, .sortedKeys])
try data.write(to: outDir.appendingPathComponent("report.json"))
print("instances=\(observation.allInstances.count) output=\(outDir.path)")
