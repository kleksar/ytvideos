import Foundation
import Vision
let url=URL(fileURLWithPath:CommandLine.arguments[1]); let handler=VNImageRequestHandler(url:url,options:[:])
let request=VNDetectHumanRectanglesRequest(); request.upperBodyOnly=false
try handler.perform([request])
for o in request.results ?? [] { print(String(format:"confidence=%.3f box=[%.3f,%.3f,%.3f,%.3f]",o.confidence,o.boundingBox.minX,o.boundingBox.minY,o.boundingBox.width,o.boundingBox.height)) }
