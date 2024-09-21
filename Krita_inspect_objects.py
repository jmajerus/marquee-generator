from krita import Krita

def get_active_document():
    """ Get the currently active Krita document. """
    app = Krita.instance()
    document = app.activeDocument()
    if not document:
        raise FileNotFoundError("No active document found. Please open a document in Krita first.")
    return document

def inspect_layer(layer, indent=0):
    """ Recursively inspect the layer and print its structure. """
    indent_str = "  " * indent
    print(f"{indent_str}Layer: {layer.name()} | Type: {layer.type()}")
    
    # If it's a vector layer, inspect the shapes in it
    if layer.type() == 'vectorlayer':
        shapes = layer.shapes()
        for shape in shapes:
            print(f"{indent_str}  Shape: {shape.type()}")
            if shape.type() == 'TextShape':
                # Print text content if it's a TextShape
                print(f"{indent_str}    Text: {shape.text()}")

    # If the layer has child layers, inspect them recursively
    for child in layer.childNodes():
        inspect_layer(child, indent + 1)

def inspect_document(document):
    """ Inspect the entire document's layers and shapes. """
    print(f"Document: {document.name()}")
    root = document.rootNode()  # Get the root node of the document
    inspect_layer(root)

# Get the active Krita document
document = get_active_document()

# Inspect the document's layers and shapes
inspect_document(document)
