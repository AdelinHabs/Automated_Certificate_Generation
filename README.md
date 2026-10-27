# Automated Certificate Generation

A Python-based tool for automatically generating personalized PDF certificates from predefined certificate templates and recipient data stored in CSV files.

The project simplifies the process of creating certificates for events, committees, individuals, and associations by automatically inserting names and relevant details into existing certificate designs. Instead of editing each certificate manually, users can generate certificates for multiple recipients in one run.

## Features

- **Multiple certificate categories:** Generate certificates for Organizing Committee members, Individuals, and Associations.
- **Batch certificate generation:** Create multiple certificates from a single CSV file.
- **Template-based design:** Use existing PNG certificate templates as backgrounds.
- **Personalized content:** Automatically add recipient names, committee positions, and association names where applicable.
- **PDF output:** Save generated certificates as PDF files.
- **Organized output:** Store generated certificates in category-specific folders.
- **Input validation:** Check for required CSV columns and missing files before processing.
- **Error handling:** Skip records with missing names and report individual certificate-generation failures.
- **High-resolution output:** Process certificate templates at 300 DPI while preserving image quality.

## How It Works

The application follows a simple workflow:

1. **Prepare recipient data:** Store recipient details in the appropriate CSV file.
2. **Select a certificate category:** Run the program and choose one of the three available certificate types.
3. **Load the template:** The program loads the corresponding PNG certificate design.
4. **Personalize certificates:** Recipient names and other relevant details are added to the template.
5. **Generate PDF files:** The program creates an individual PDF certificate for each valid recipient.
6. **Save the results:** The generated certificates are saved in the output directory.

## Certificate Categories

| Category | Required CSV columns | Template |
|---|---|---|
| Organizing Committee | `NAME`, `POST` | `OrganizingCommittee.png` |
| Individual | `NAME`, `ASSOCIATION` | `Individual.png` |
| Association | `NAME` | `Association.png` |

## Technologies Used

- **Python** — Core programming language.
- **Pandas** — Reads and processes recipient data from CSV files.
- **Pillow (PIL)** — Loads certificate templates and draws personalized text.
- **img2pdf** — Converts the processed certificate images into PDF files.

## Project Structure

The application expects the following supporting files and directories. The data and template files must be created or supplied separately if they are not included in the repository.

```text
Automated_Certificate_Generation/
├── main.py
├── Data/
│   ├── Organizing_Committee.csv
│   ├── Individual.csv
│   └── Association.csv
├── Templates/
│   ├── OrganizingCommittee.png
│   ├── Individual.png
│   └── Association.png
└── Certificates_Done/
    ├── 1/
    ├── 2/
    └── 3/
```

**Note:** `main.py` is the primary certificate-generation script described in this README. The other Python files contain separate image-generation workflows and may require additional configuration.

## Requirements

- Python 3.9 or later recommended.
- Pandas
- Pillow
- img2pdf
- The appropriate PNG certificate templates.
- The font file configured in the script.
- CSV files containing the recipient information.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AdelinHabs/Automated_Certificate_Generation.git
cd Automated_Certificate_Generation
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install pandas pillow img2pdf
```

## Configuration

Before running the program, update the file paths in `main.py` to match your computer.

Configure:

- `base_folder` — The main directory containing the project data and templates.
- `font_path` — The location of the font used on the certificates.
- `templates_folder` — The directory containing the PNG certificate templates.
- `output_folder` — The directory where the generated PDF certificates will be stored.

Ensure that each CSV file contains the required column names and that the corresponding templates and font file exist.

### Example CSV Data

**Organizing_Committee.csv**

```csv
NAME,POST
Jane Doe,Chairperson
John Smith,Secretary
Mary Johnson,Treasurer
```

**Individual.csv**

```csv
NAME,ASSOCIATION
Jane Doe,Computer Science Association
John Smith,Engineering Association
```

**Association.csv**

```csv
NAME
Computer Science Association
Engineering Association
```

Use your actual recipient information and ensure the column headers match the requirements for the selected category.

## Usage

Run the main application:

```bash
python main.py
```

The program will display a menu:

```text
Choose a certificate type:

1. Organizing Committee
2. Individual
3. Association
```

Enter the number corresponding to the certificate category you want to generate.

The application will read the appropriate CSV file, personalize the selected template, and generate a PDF certificate for each valid record.

## Output

Generated certificates are saved in the `Certificates_Done` directory, organized by category:

- `Certificates_Done/1/` — Organizing Committee certificates.
- `Certificates_Done/2/` — Individual certificates.
- `Certificates_Done/3/` — Association certificates.

Each certificate is saved as an individual PDF file named after its recipient.

**Important:** If a generated certificate already exists with the same filename, it may be overwritten. Back up existing certificates before regenerating them.

## Error Handling and Limitations

- Missing CSV files, templates, or font files must be resolved before generation can proceed.
- CSV files must contain the required columns for the selected certificate category.
- Certificate text positions, font sizes, and colors are configured in the code and may need adjustment to match different templates.
- The file paths in the current implementation are configured for a particular Windows environment and must be updated before use on another computer.
- The project currently uses predefined templates rather than providing a graphical interface for designing certificates.

## Future Improvements

Potential enhancements include:

- A graphical user interface for selecting files and certificate types.
- Configurable templates, fonts, and text positioning.
- Support for Excel input files.
- A progress indicator and generation summary.
- Automatic detection of duplicate recipients and existing certificates.
- More flexible output formats and directory settings.
- A configuration file to eliminate hard-coded paths.

## Contributing

Contributions, suggestions, and bug reports are welcome. You can fork the repository, make improvements, and submit a pull request.

## License

No license is currently specified in the repository. Please add an appropriate open-source license before distributing or reusing the project under specific licensing terms.

## Author

**AdelinHabs**

GitHub: https://github.com/AdelinHabs

## Acknowledgements

This project demonstrates how Python can automate repetitive document-generation tasks, reduce manual effort, and make producing personalized certificates for events and organizations more efficient.
