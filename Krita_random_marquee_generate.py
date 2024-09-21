import os
import re
import random
from xml.dom import minidom
from krita import Krita

def get_active_document():
    """ Get the currently active Krita document. """
    app = Krita.instance()
    document = app.activeDocument()
    if not document:
        raise FileNotFoundError("No active document found. Please open a document in Krita first.")
    return document

def update_text_in_shape(layer, new_text_lines):
    """ Update the text in KoSvgTextShapeID objects inside a vector layer, preserving existing formatting and line breaks. """
    svgHeader = re.compile('(^.*?\<svg.*?["\']\\s*\>).*$', re.DOTALL).sub(r'\1', layer.toSvg())

    for shape in layer.shapes():
        if shape.type() == 'KoSvgTextShapeID':
            # Extract SVG content
            svgContent = svgHeader + shape.toSvg(True, False) + '</svg>'
            svgDom = minidom.parseString(svgContent)

            # Find the tspan elements
            tspan_elements = svgDom.getElementsByTagName("tspan")
            if not tspan_elements:
                raise ValueError("No tspan elements found in the text object.")
            
            # Clear existing tspans' text, but preserve the formatting attributes
            for tspan in tspan_elements:
                tspan.firstChild.nodeValue = ""  # Clear existing text

            # Apply the new text lines while maintaining the existing formatting attributes
            for index, line in enumerate(new_text_lines):
                if index < len(tspan_elements):
                    # Reuse existing tspans if fewer lines than tspans
                    tspan = tspan_elements[index]
                else:
                    # Create new tspan elements if there are more lines than existing tspans
                    tspan = svgDom.createElement("tspan")
                    tspan.setAttribute("x", tspan_elements[0].getAttribute("x"))  # Use x-position from the first tspan
                    tspan.setAttribute("dy", tspan_elements[0].getAttribute("dy"))  # Use dy from the first tspan
                    svgDom.getElementsByTagName("text")[0].appendChild(tspan)
                
                # Set the new text content for each line
                tspan.firstChild.nodeValue = line

            # Remove the old shape and add the updated SVG content back
            shape.remove()  # Remove the old shape
            layer.addShapesFromSvg(svgDom.toxml())  # Re-add the updated shape

            print("Updated Text Successfully with Line Breaks and Preserved Formatting!")
            return  # Stop after updating the first text shape

def update_text_layer(document, layer_name, text_lines):
    """ Update the specified vector layer's text using SVG manipulation, preserving formatting. """
    layer = document.nodeByName(layer_name)
    if layer and layer.type() == 'vectorlayer':
        print(f"Found layer: {layer_name}, clearing existing text and updating...")
        update_text_in_shape(layer, text_lines)  # Pass lines as a list
    else:
        raise ValueError(f"Layer {layer_name} not found or is not a vector layer.")

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the text file
text_file_path = os.path.join(current_dir, "text_file.txt")

# Get the active Krita document
document = get_active_document()

# Read all lines from the text file and filter out blank lines
with open(text_file_path, "r") as file:
    lines = [line.strip() for line in file.readlines() if line.strip()]  # Ignore blank lines

# Select 5 random lines from the text file
if len(lines) < 5:
    raise ValueError("The text file must contain at least 5 non-blank lines.")
random_lines = random.sample(lines, 5)

# Update the MARQUEE layer with the selected random lines (with line breaks)
update_text_layer(document, "MARQUEE", random_lines)

print("Random lines placed in MARQUEE with line breaks and preserved formatting. You can now save the document manually.")
