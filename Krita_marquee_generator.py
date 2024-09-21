from krita import Krita, Document, InfoObject

def load_document(file_path):
    """ Load the Krita document. """
    app = Krita.instance()
    document = app.openDocument(file_path)
    if not document:
        raise FileNotFoundError("The specified document could not be loaded.")
    return document

def update_text_layer(document, layer_name, text):
    """ Update the specified text layer with new text, preserving line breaks. """
    layer = document.nodeByName(layer_name)
    if layer and layer.type() == 'vectorlayer':
        # Ensure that line breaks within text are preserved
        layer.setPlainText(text)
    else:
        raise ValueError(f"Layer {layer_name} not found or is not a text layer.")

def export_image(document, file_name):
    """ Export the document to a PNG file. """
    info = InfoObject()
    info.setProperty("format", "PNG")
    document.exportImage(file_name, info)
    print(f"Exported {file_name}")

def pause_script():
    """ Pause the script for manual editing. """
    input("Edit the image as needed in Krita, then press Enter to continue...")

# Path to your Krita document and text file
doc_path = "path_to_your_kra_document.kra"
text_file_path = "path_to_your_text_file.txt"

# Load the document
document = load_document(doc_path)

# Ensure the document stays open while the script runs
document.setActive(True)

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
