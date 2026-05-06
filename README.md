# PDF Splitter

A simple, beginner-friendly desktop application built with Python and Tkinter that allows users to split PDF files by extracting specific page ranges.

## Features
- **Clean UI**: Minimal and intuitive graphical user interface.
- **Select PDF**: Easily browse and select the PDF file you want to split.
- **Flexible Page Ranges**: Input specific pages or ranges (e.g., `1-3, 5, 8-10`) to extract.
- **Output Folder Selection**: Choose exactly where you want to save your newly split PDF.
- **File Information**: Automatically displays the total number of pages of the selected PDF.
- **Graceful Error Handling**: Validates invalid page ranges and handles missing files gracefully.

## Requirements
- Python 3.x
- PyPDF2 (>=3.0.0)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Soutikkk/PDF_Splitter.git
   cd PDF_Splitter
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python pdf_splitter.py
   ```
2. Click **Browse PDF** to select a PDF file from your computer.
3. Enter the pages you wish to extract in the **Pages to extract** text box (e.g., `1-3, 5, 8-10`).
4. Click **Browse Folder** to choose an output destination.
5. Click **Split PDF**. The app will extract the requested pages and save them to your selected folder as `split_output.pdf`.
