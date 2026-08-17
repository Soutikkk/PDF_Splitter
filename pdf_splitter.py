import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import PyPDF2


class PDFSplitterApp:
    """GUI application for extracting selected pages from a PDF."""

    def __init__(self, root):
        self.root = root

        # Window configuration
        self.root.title("PDF Splitter")
        self.root.geometry("560x450")
        self.root.resizable(False, False)

        # Variables
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.total_pages = tk.IntVar(value=0)
        self.status_text = tk.StringVar(value="Select a PDF file to begin.")

        self.setup_style()
        self.setup_ui()

    # ---------------------------------------------------------
    # UI SETUP
    # ---------------------------------------------------------

    def setup_style(self):
        """Configure ttk styles."""

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 18, "bold")
        )

        style.configure(
            "Info.TLabel",
            font=("Arial", 10)
        )

        style.configure(
            "Split.TButton",
            font=("Arial", 11, "bold")
        )

    def setup_ui(self):
        """Create all GUI components."""

        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main_frame,
            text="PDF Splitter",
            style="Title.TLabel"
        ).pack(pady=(0, 5))

        ttk.Label(
            main_frame,
            text="Extract specific pages from a PDF",
            style="Info.TLabel"
        ).pack(pady=(0, 20))

        # -----------------------------------------------------
        # PDF SELECTION
        # -----------------------------------------------------

        pdf_frame = ttk.LabelFrame(
            main_frame,
            text="1. Select PDF",
            padding=12
        )
        pdf_frame.pack(fill="x", pady=5)

        pdf_input_frame = ttk.Frame(pdf_frame)
        pdf_input_frame.pack(fill="x")

        self.pdf_entry = ttk.Entry(
            pdf_input_frame,
            textvariable=self.pdf_path,
            state="readonly"
        )
        self.pdf_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ttk.Button(
            pdf_input_frame,
            text="Browse",
            command=self.browse_pdf
        ).pack(side="right")

        self.info_label = ttk.Label(
            pdf_frame,
            text="Total Pages: 0"
        )
        self.info_label.pack(anchor="w", pady=(8, 0))

        # -----------------------------------------------------
        # PAGE RANGE
        # -----------------------------------------------------

        range_frame = ttk.LabelFrame(
            main_frame,
            text="2. Select Pages",
            padding=12
        )
        range_frame.pack(fill="x", pady=10)

        ttk.Label(
            range_frame,
            text="Enter page numbers or ranges:"
        ).pack(anchor="w")

        self.range_entry = ttk.Entry(range_frame)
        self.range_entry.pack(fill="x", pady=(5, 3))

        ttk.Label(
            range_frame,
            text="Example: 1-3, 5, 8-10",
            foreground="gray"
        ).pack(anchor="w")

        # -----------------------------------------------------
        # OUTPUT FOLDER
        # -----------------------------------------------------

        output_frame = ttk.LabelFrame(
            main_frame,
            text="3. Output Folder",
            padding=12
        )
        output_frame.pack(fill="x", pady=5)

        output_input_frame = ttk.Frame(output_frame)
        output_input_frame.pack(fill="x")

        self.output_entry = ttk.Entry(
            output_input_frame,
            textvariable=self.output_dir,
            state="readonly"
        )
        self.output_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ttk.Button(
            output_input_frame,
            text="Browse",
            command=self.browse_output_folder
        ).pack(side="right")

        # -----------------------------------------------------
        # PROGRESS BAR
        # -----------------------------------------------------

        self.progress = ttk.Progressbar(
            main_frame,
            mode="determinate",
            maximum=100
        )
        self.progress.pack(fill="x", pady=(15, 5))

        # Status
        ttk.Label(
            main_frame,
            textvariable=self.status_text
        ).pack()

        # -----------------------------------------------------
        # SPLIT BUTTON
        # -----------------------------------------------------

        self.split_button = ttk.Button(
            main_frame,
            text="Split PDF",
            command=self.split_pdf,
            style="Split.TButton",
            state="disabled"
        )
        self.split_button.pack(pady=15, ipadx=25, ipady=5)

    # ---------------------------------------------------------
    # FILE SELECTION
    # ---------------------------------------------------------

    def browse_pdf(self):
        """Select a PDF file."""

        file_path = filedialog.askopenfilename(
            title="Select a PDF File",
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        self.pdf_path.set(file_path)
        self.update_pdf_info(file_path)

    def browse_output_folder(self):
        """Select the output directory."""

        folder_path = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder_path:
            self.output_dir.set(folder_path)
            self.update_button_state()

    # ---------------------------------------------------------
    # PDF INFORMATION
    # ---------------------------------------------------------

    def update_pdf_info(self, file_path):
        """Read the PDF and display the total number of pages."""

        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)

                total_pages = len(reader.pages)

                if total_pages == 0:
                    raise ValueError("The selected PDF contains no pages.")

                self.total_pages.set(total_pages)

                self.info_label.config(
                    text=f"Total Pages: {total_pages}"
                )

                self.status_text.set(
                    "PDF loaded successfully."
                )

                # Automatically select the same folder as output
                if not self.output_dir.get():
                    self.output_dir.set(
                        str(Path(file_path).parent)
                    )

                self.update_button_state()

        except Exception as error:
            messagebox.showerror(
                "Unable to Read PDF",
                f"Could not read the selected PDF.\n\n{error}"
            )

            self.pdf_path.set("")
            self.total_pages.set(0)

            self.info_label.config(
                text="Total Pages: 0"
            )

            self.status_text.set(
                "Failed to load PDF."
            )

            self.update_button_state()

    # ---------------------------------------------------------
    # BUTTON STATE
    # ---------------------------------------------------------

    def update_button_state(self):
        """Enable Split button only when required data exists."""

        if (
            self.pdf_path.get()
            and self.output_dir.get()
            and self.total_pages.get() > 0
        ):
            self.split_button.config(state="normal")
        else:
            self.split_button.config(state="disabled")

    # ---------------------------------------------------------
    # PAGE RANGE PARSING
    # ---------------------------------------------------------

    def parse_page_ranges(self, range_string, max_pages):
        """
        Convert page input such as:

            1-3, 5, 8-10

        into zero-based page indexes.

        Example:
            1-3 -> [0, 1, 2]
        """

        pages = set()

        # Remove spaces
        range_string = range_string.replace(" ", "")

        if not range_string:
            raise ValueError("Please enter the pages to extract.")

        parts = range_string.split(",")

        for part in parts:

            if not part:
                raise ValueError("Invalid page range format.")

            # Range: 1-5
            if "-" in part:

                bounds = part.split("-")

                if len(bounds) != 2:
                    raise ValueError(
                        f"Invalid range: {part}"
                    )

                start_text, end_text = bounds

                if not start_text or not end_text:
                    raise ValueError(
                        f"Invalid range: {part}"
                    )

                try:
                    start = int(start_text)
                    end = int(end_text)
                except ValueError:
                    raise ValueError(
                        f"Page numbers must be integers: {part}"
                    )

                if start > end:
                    raise ValueError(
                        f"Start page cannot be greater than end page: {part}"
                    )

                if start < 1 or end > max_pages:
                    raise ValueError(
                        f"Pages must be between 1 and {max_pages}: {part}"
                    )

                for page in range(start, end + 1):
                    pages.add(page - 1)

            # Single page: 5
            else:

                try:
                    page = int(part)
                except ValueError:
                    raise ValueError(
                        f"Page number must be an integer: {part}"
                    )

                if page < 1 or page > max_pages:
                    raise ValueError(
                        f"Page {page} does not exist. "
                        f"Choose between 1 and {max_pages}."
                    )

                pages.add(page - 1)

        if not pages:
            raise ValueError(
                "No valid pages were specified."
            )

        return sorted(pages)

    # ---------------------------------------------------------
    # PDF SPLITTING
    # ---------------------------------------------------------

    def split_pdf(self):
        """Extract selected pages and create a new PDF."""

        input_pdf = self.pdf_path.get()
        output_folder = self.output_dir.get()
        range_string = self.range_entry.get()

        # Basic validation
        if not input_pdf:
            messagebox.showwarning(
                "Missing PDF",
                "Please select a PDF file."
            )
            return

        if not output_folder:
            messagebox.showwarning(
                "Missing Output Folder",
                "Please select an output folder."
            )
            return

        if not range_string.strip():
            messagebox.showwarning(
                "Missing Pages",
                "Please enter the pages you want to extract."
            )
            return

        # Parse pages
        try:
            pages = self.parse_page_ranges(
                range_string,
                self.total_pages.get()
            )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Page Range",
                str(error)
            )
            return

        # Start progress
        self.progress["value"] = 0
        self.root.update_idletasks()

        try:
            with open(input_pdf, "rb") as input_file:

                reader = PyPDF2.PdfReader(input_file)
                writer = PyPDF2.PdfWriter()

                total_selected = len(pages)

                for index, page_number in enumerate(pages):

                    writer.add_page(
                        reader.pages[page_number]
                    )

                    progress = (
                        (index + 1) / total_selected
                    ) * 100

                    self.progress["value"] = progress
                    self.status_text.set(
                        f"Processing page {page_number + 1}..."
                    )

                    self.root.update_idletasks()

                # Create output filename
                input_name = Path(input_pdf).stem

                output_path = (
                    Path(output_folder)
                    / f"{input_name}_split.pdf"
                )

                # Avoid overwriting an existing file
                output_path = self.get_unique_output_path(
                    output_path
                )

                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

            self.progress["value"] = 100

            self.status_text.set(
                f"Successfully extracted {len(pages)} page(s)."
            )

            messagebox.showinfo(
                "Success",
                "PDF created successfully!\n\n"
                f"Pages extracted: {len(pages)}\n"
                f"Saved to:\n{output_path}"
            )

        except Exception as error:

            self.progress["value"] = 0

            self.status_text.set(
                "Failed to split PDF."
            )

            messagebox.showerror(
                "Error",
                f"An error occurred while splitting the PDF:\n\n{error}"
            )

    # ---------------------------------------------------------
    # OUTPUT FILE HANDLING
    # ---------------------------------------------------------

    @staticmethod
    def get_unique_output_path(path):
        """
        Prevent overwriting an existing output file.

        Example:

            report_split.pdf
            report_split_1.pdf
            report_split_2.pdf
        """

        if not path.exists():
            return path

        counter = 1

        while True:

            new_path = (
                path.parent
                / f"{path.stem}_{counter}{path.suffix}"
            )

            if not new_path.exists():
                return new_path

            counter += 1


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------

def main():
    root = tk.Tk()

    PDFSplitterApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
