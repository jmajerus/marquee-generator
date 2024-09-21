import os
import re
from xml.dom import minidom
from krita import Krita

def get_active_document():
    """ Get the currently active Krita document. """
    app = Krita.instance()
    document = app.activeDocument()
    if not document:
        raise FileNotFoundError("No active document found. Please open a document in Krita first.")
    return document

def update_text_in_shape(layer, new_text):
    """ Update the text in KoSvgTextShapeID objects inside a vector layer. """
    svgHeader = re.compile('(^.*?\<svg.*?["\']\\s*\>).*$', re.DOTALL).sub(r'\1', layer.toSvg())

    for shape in layer.shapes():
        if shape.type() == 'KoSvgTextShapeID':
            # Extract SVG content
            svgContent = svgHeader + shape.toSvg(True, False) + '</svg>'
            svgDom = minidom.parseString(svgContent)

            # Find and update the tspan elements with new text
            for node in svgDom.getElementsByTagName("tspan"):
                print(f"Original Text: {node.firstChild.nodeValue}")
                node.firstChild.nodeValue = new_text  # Set new text

            # Remove the old shape and add the updated SVG content back
            shape.remove()  # Remove the old shape
            layer.addShapesFromSvg(svgDom.toxml())  # Re-add the updated shape

            print("Updated Text Successfully!")
            return  # Stop after updating the first text shape

def update_text_layer(document, layer_name, text):
    """ Update the specified vector layer's text using SVG manipulation. """
    layer = document.nodeByName(layer_name)
    if layer and layer.type() == 'vectorlayer':
        print(f"Found layer: {layer_name}, updating text...")
        update_text_in_shape(layer, text)
    else:
        raise ValueError(f"Layer {layer_name} not found or is not a vector layer.")

def export_image(document, file_name):
    """ Export the document to a PNG file using Krita's InfoObject. """
    info = document.createExportInfo()  # Correctly create the InfoObject
    info.setMimeType("image/png")  # Set the output format to PNG
    success = document.exportImage(file_name, info)
    
    if success:
        print(f"Exported {file_name}")
    else:
        print(f"Failed to export {file_name}")


# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the text file
text_file_path = os.path.join(current_dir, "marquee.txt")

# Get the active Krita document
document = get_active_document()

# Read the text file and process each block
try:
    with open(text_file_path, "r") as file:
        text_blocks = file.read().strip().split("\n\n")  # Split text into blocks

    for index, block in enumerate(text_blocks):
        lines = block.split("\n")
        update_text_layer(document, "MAIN", lines[0])
        if len(lines) > 1:
            update_text_layer(document, "MARQUEE", "\n".join(lines[1:]))

        # Export immediately without pausing
        export_image(document, f"output_{index+1:03d}.png")
finally:
    document.close()  # Close the document after processing all blocks
