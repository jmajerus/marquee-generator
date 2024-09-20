# Marquee Generator

A Python-Fu script for GIMP that allows you to dynamically generate and modify marquee text layers, enabling easy text replacement and exporting to PNG format.

## Features

- Replace text in **MAIN** and **MARQUEE** layers dynamically.
- Group lines of text by blank lines and automatically assign text to layers.
- Allows for manual editing between iterations before exporting images.
- Automatically exports images with a configurable naming convention.
- Supports seamless text updates within GIMP without saving changes to the original .XCF file.

## Getting Started

### Prerequisites

- **GIMP**: Install GIMP, the GNU Image Manipulation Program. [Download GIMP](https://www.gimp.org/downloads/)
- **Python-Fu**: Ensure that Python-Fu is enabled in GIMP.
- **Git**: Optional, for version control and contributing to the repository. [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Installation

1.  Clone the repository to your local machine:

    git clone https://github.com/YourGitHubUsername/marquee-generator.git
    

2.  Copy the Python script (`replace_text_in_layers_and_export.py`) into your GIMP scripts folder:
    *   **Windows**: `C:\Users\YourUserName\AppData\Roaming\GIMP\2.10\scripts`
    *   **Linux**: `~/.config/GIMP/2.10/scripts/`
    *   **macOS**: `~/Library/Application Support/GIMP/2.10/scripts/`
3.  Restart GIMP to load the script.

### Usage

1.  Open a GIMP project that contains text layers named **MAIN** and **MARQUEE**.
2.  Use the Python-Fu menu in GIMP to access the **Replace Text in Layers and Export** script.
3.  Provide a text file where groups of lines are separated by blank lines:
    *   The first line of each group will populate the **MAIN** layer.
    *   Subsequent lines will populate the **MARQUEE** layer.
4.  The script will pause after each iteration to allow for manual edits in GIMP.
5.  Once the edits are done, the script will export the image as a PNG.

### Example

Here's an example of how the text file should be structured:

    Title for Group 1
    Line 1 of Marquee for Group 1
    Line 2 of Marquee for Group 1
    
    Title for Group 2
    Line 1 of Marquee for Group 2
    
    Title for Group 3
    

Each block of text between blank lines represents a group, and the first line of each group is assigned to the **MAIN** layer, while subsequent lines are assigned to the **MARQUEE** layer.

### Example Output

![Marquee Example](./images/marquee-example.png)


### Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or bug fixes.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Make your changes and commit them (`git commit -m "Add new feature"`).
4.  Push to the branch (`git push origin feature-branch`).
5.  Open a pull request.

### License

This project is licensed under the MIT License - see the `[LICENSE](LICENSE)` file for details.

### Contact

If you have any questions, feel free to contact the project maintainer:

**John Majerus**

*   Email: `jmajerus@acm.org`
*   GitHub: [John Majerus](https://github.com/jmajerus)
