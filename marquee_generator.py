from gimpfu import *
import os

def replace_text_in_layers_and_export(image, text_file, output_folder):
    # Read all lines from the text file
    with open(text_file, 'r') as file:
        # Split the file content into groups separated by blank lines
        groups = []
        current_group = []
        for line in file:
            stripped_line = line.strip()
            if stripped_line == "":  # Blank line signals end of group
                if current_group:  # Save the current group if not empty
                    groups.append(current_group)
                    current_group = []
            else:
                current_group.append(stripped_line)

        if current_group:  # Add the last group if any
            groups.append(current_group)

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Find the "MAIN" and "MARQUEE" layers
    main_layer = None
    marquee_layer = None

    for layer in image.layers:
        if layer.name == "MAIN":
            main_layer = layer
        elif layer.name == "MARQUEE":
            marquee_layer = layer

    if not main_layer or not marquee_layer:
        gimp.message("Both 'MAIN' and 'MARQUEE' layers must exist in the image.")
        return

    # Start undo group to batch the operations
    pdb.gimp_image_undo_group_start(image)

    # Process each group of lines
    for iteration, group in enumerate(groups):
        if len(group) > 0:
            # The first line goes into the "MAIN" text layer
            main_text = group[0]
            pdb.gimp_text_layer_set_text(main_layer, main_text)

        if len(group) > 1:
            # The remaining lines go into the "MARQUEE" text layer
            marquee_text = "\n".join(group[1:])
            pdb.gimp_text_layer_set_text(marquee_layer, marquee_text)
        else:
            # Clear the "MARQUEE" layer if there are no subsequent lines
            pdb.gimp_text_layer_set_text(marquee_layer, "")

        # Prompt the user to pause for manual editing
        gimp.message(f"MAIN text updated to:\n{main_text}\n\nMARQUEE text updated to:\n{marquee_text}\nMake manual adjustments, then press OK to export.")
        pdb.gimp_displays_flush()  # Ensure GIMP displays are updated

        # Wait for user confirmation before proceeding
        pdb.gimp_message("Click OK after manual editing is complete to proceed with export.")

        # Define the output filename (incremented for each iteration)
        output_file = os.path.join(output_folder, f"output_image_{iteration+1}.png")

        # Export the image to PNG
        pdb.file_png_save_defaults(image, image.active_layer, output_file, output_file)

    # End the undo group to avoid saving changes
    pdb.gimp_image_undo_group_end(image)

# Register the script in GIMP's menu
register(
    "python_fu_replace_text_in_layers_and_export",
    "Replace Text in MAIN and MARQUEE Layers and Export to PNG",
    "Replaces text in 'MAIN' and 'MARQUEE' text layers from a file, with the first line going to 'MAIN' and subsequent lines to 'MARQUEE', pauses for manual editing, and exports each version as a PNG without saving the original image.",
    "John Majerus", "John Majerus", "2024",
    "<Image>/Python-Fu/Replace Text in Layers and Export",  # Menu location
    "*",  # Image types
    [
        (PF_FILE, "text_file", "Text File Path", ""),  # Input file with text lines
        (PF_DIRNAME, "output_folder", "Output Folder", "")  # Folder to save PNGs
    ],
    [],
    replace_text_in_layers_and_export
)

# Start the script
main()
