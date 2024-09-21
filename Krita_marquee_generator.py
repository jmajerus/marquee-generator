import os
from krita import Krita, InfoObject

def get_active_document():
    """ Get the currently active Krita document. """
    app = Krita.instance()
    document = app.activeDocument()
    if not document:
        raise FileNotFoundError("No active document found. Please open a document in Krita first.")
    return document

def update_text_layer(document, layer_name, text):
    """ Update the text shape in the specified vector layer with new text, preserving line breaks. """
    layer = document.nodeByName(layer_name)
    if layer and layer.type() == 'vectorlayer':
        # Iterate over the shapes in the vector layer to find the TextShape
        for shape in layer.shapes():
            if shape.type() == 'TextShape':
                shape.setText(text)  # Set the new text in the text shape
                break
        else:
            raise ValueError(f"No text shape found in layer {layer_name}.")
    else:
        raise ValueError(f"Layer {layer_name} not found or is not a vector layer.")

def export_image(document, file_name):
    """ Export the document to a PNG file. """
    info = InfoObject()
    info.setProperty("format", "PNG")
    document.exportImage(file_name, info)
    print(f"Exported {file_name}")

def pause_script():
    """ Pause the script for manual editing. """
    input("Edit the image as needed in Krita, then press Enter to continue...")

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

        pause_script()  # Manual edit prompt
        export_image(document, f"output_{index+1:03d}.png")
finally:
    document.close()  # Close the document after processing all blocks
