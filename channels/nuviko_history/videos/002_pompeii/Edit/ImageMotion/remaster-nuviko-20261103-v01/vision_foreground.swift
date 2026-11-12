import Foundation
import Vision
import ImageIO
import CoreImage

struct Scene: Decodable { let scene: Int; let image: String }
let args = CommandLine.arguments
if args.count != 3 { fatalError("usage: vision_foreground.swift MANIFEST OUTDIR") }
let manifestURL = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2], isDirectory: true)
try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
let scenes = try JSONDecoder().decode([Scene].self, from: Data(contentsOf: manifestURL))
let context = CIContext(options: nil)
var reports: [[String: Any]] = []
for scene in scenes {
    let imageURL = URL(fileURLWithPath: scene.image)
    let handler = VNImageRequestHandler(url: imageURL, options: [:])
    let humanRequest = VNDetectHumanRectanglesRequest()
    humanRequest.upperBodyOnly = false
    try handler.perform([humanRequest])
    let humans = (humanRequest.results ?? []).filter { $0.confidence >= 0.35 }
    var method = "foreground-instance"
    var maskCI: CIImage? = nil
    if !humans.isEmpty {
        let personRequest = VNGeneratePersonInstanceMaskRequest()
        try handler.perform([personRequest])
        if let observation = personRequest.results?.first as? VNInstanceMaskObservation,
           !observation.allInstances.isEmpty {
            maskCI = CIImage(cvPixelBuffer: try observation.generateScaledMaskForImage(
                forInstances: observation.allInstances, from: handler))
            method = "person-instance"
        }
    }
    if maskCI == nil {
        let objectRequest = VNGenerateForegroundInstanceMaskRequest()
        try handler.perform([objectRequest])
        if let observation = objectRequest.results?.first as? VNInstanceMaskObservation,
           !observation.allInstances.isEmpty {
            maskCI = CIImage(cvPixelBuffer: try observation.generateScaledMaskForImage(
                forInstances: observation.allInstances, from: handler))
        }
    }
    guard let maskCI, let cg = context.createCGImage(maskCI, from: maskCI.extent) else {
        reports.append(["scene": scene.scene, "status": "NO_MASK", "method": method,
                        "image": imageURL.path, "humans": humans.count])
        continue
    }
    let basename = String(format: "S%03d", scene.scene)
    let output = outDir.appendingPathComponent(basename + ".png")
    guard let destination = CGImageDestinationCreateWithURL(output as CFURL, "public.png" as CFString, 1, nil) else {
        fatalError("Could not create image output for scene \(scene.scene)")
    }
    CGImageDestinationAddImage(destination, cg, nil)
    guard CGImageDestinationFinalize(destination) else { fatalError("Could not save mask for scene \(scene.scene)") }
    reports.append(["scene": scene.scene, "status": "MASK_READY", "method": method,
                    "image": imageURL.path, "mask": output.path,
                    "mask_width": cg.width, "mask_height": cg.height, "humans": humans.count,
                    "human_boxes": humans.map { ["confidence": $0.confidence,
                        "x": $0.boundingBox.minX, "y": $0.boundingBox.minY,
                        "width": $0.boundingBox.width, "height": $0.boundingBox.height] }])
    print("S\(String(format: "%03d", scene.scene)) \(method) mask \(cg.width)x\(cg.height) humans=\(humans.count)")
}
let data = try JSONSerialization.data(withJSONObject: reports, options: [.prettyPrinted, .sortedKeys])
try data.write(to: outDir.appendingPathComponent("vision_receipt.json"))
print("saved \(reports.count) mask records to \(outDir.path)")
