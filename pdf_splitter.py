
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from pypdf import PdfReader, PdfWriter


class PDFSplitterApp:
    """A GUI application for extracting selected pages from PDF files."""

    def __init__(self, root):
        self.root = root

        self.root.title("PDF Splitter")
        self.root.geometry("560x460")
        self.root.resizable(False, False)

        # Application variables
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.total_pages = tk.IntVar(value=0)
        self.status_text = tk.StringVar(
            value="Select a PDF file to begin."
        )

        self.setup_style()
        self.setup_ui()

    # --------------------------------------------------
    # STYLING
    # --------------------------------------------------

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 19, "bold")
        )

        style.configure(
            "Info.TLabel",
            font=("Arial", 10)
        )

        style.configure(
            "Split.TButton",
            font=("Arial", 11, "bold")
        )

    # --------------------------------------------------
    # USER INTERFACE
    # --------------------------------------------------

    def setup_ui(self):

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Application title
        ttk.Label(
            main_frame,
            text="PDF Splitter",
            style="Title.TLabel"
        ).pack(pady=(0, 5))

        ttk.Label(
            main_frame,
            text="Extract specific pages from a PDF document",
            style="Info.TLabel"
        ).pack(pady=(0, 20))

        # PDF selection
        pdf_frame = ttk.LabelFrame(
            main_frame,
            text="1. Select PDF",
            padding=12
        )
        pdf_frame.pack(fill="x", pady=5)

        pdf_input_frame = ttk.Frame(pdf_frame)
        pdf_input_frame.pack(fill="x")

        ttk.Entry(
            pdf_input_frame,
            textvariable=self.pdf_path,
            state="readonly"
        ).pack(
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

        # Page selection
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

        # Output folder selection
        output_frame = ttk.LabelFrame(
            main_frame,
            text="3. Output Folder",
            padding=12
        )
        output_frame.pack(fill="x", pady=5)

        output_input_frame = ttk.Frame(output_frame)
        output_input_frame.pack(fill="x")

        ttk.Entry(
            output_input_frame,
            textvariable=self.output_dir,
            state="readonly"
        ).pack(
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

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode="determinate",
            maximum=100
        )
        self.progress.pack(fill="x", pady=(15, 5))

        # Status message
        ttk.Label(
            main_frame,
            textvariable=self.status_text
        ).pack()

        # Split button
        self.split_button = ttk.Button(
            main_frame,
            text="Split PDF",
            command=self.split_pdf,
            style="Split.TButton",
            state="disabled"
        )
        self.split_button.pack(pady=15, ipadx=25, ipady=5)

    # --------------------------------------------------
    # FILE SELECTION
    # --------------------------------------------------

    def browse_pdf(self):

        file_path = filedialog.askopenfilename(
            title="Select a PDF File",
            filetypes=[
                ("PDF Files", "*.pdf")
            ]
        )

        if not file_path:
            return

        self.pdf_path.set(file_path)
        self.update_pdf_info(file_path)

    def browse_output_folder(self):

        folder_path = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder_path:
            self.output_dir.set(folder_path)
            self.update_button_state()

    # --------------------------------------------------
    # PDF INFORMATION
    # --------------------------------------------------

    def update_pdf_info(self, file_path):

        try:
            reader = PdfReader(file_path)

            if reader.is_encrypted:
                raise ValueError(
                    "This PDF is password-protected."
                )

            total_pages = len(reader.pages)

            if total_pages == 0:
                raise ValueError(
                    "The selected PDF contains no pages."
                )

            self.total_pages.set(total_pages)

            self.info_label.config(
                text=f"Total Pages: {total_pages}"
            )

            self.status_text.set(
                "PDF loaded successfully."
            )

            # Set default output directory
            if not self.output_dir.get():
                self.output_dir.set(
                    str(Path(file_path).parent)
                )

            self.update_button_state()

        except Exception as error:

            self.pdf_path.set("")
            self.total_pages.set(0)

            self.info_label.config(
                text="Total Pages: 0"
            )

            self.status_text.set(
                "Failed to load PDF."
            )

            self.update_button_state()

            messagebox.showerror(
                "Unable to Read PDF",
                f"Could not read the selected PDF.\n\n{error}"
            )

    # --------------------------------------------------
    # BUTTON STATE
    # --------------------------------------------------

    def update_button_state(self):

        if (
            self.pdf_path.get()
            and self.output_dir.get()
            and self.total_pages.get() > 0
        ):
            self.split_button.config(state="normal")

        else:
            self.split_button.config(state="disabled")

    # --------------------------------------------------
    # PAGE RANGE PARSING
    # --------------------------------------------------

    @staticmethod
    def parse_page_ranges(range_string, max_pages):
        """
        Convert page ranges into zero-based indexes.

        Examples:
            1-3       -> [0, 1, 2]
            5         -> [4]
            1-3, 5    -> [0, 1, 2, 4]
            1-3, 5-7  -> [0, 1, 2, 4, 5, 6]
        """

        if not range_string.strip():
            raise ValueError(
                "Please enter the pages to extract."
            )

        pages = set()

        parts = range_string.split(",")

        for part in parts:

            part = part.strip()

            if not part:
                raise ValueError(
                    "Invalid page range format."
                )

            if "-" in part:

                bounds = part.split("-")

                if len(bounds) != 2:
                    raise ValueError(
                        f"Invalid range: {part}"
                    )

                try:
                    start = int(bounds[0].strip())
                    end = int(bounds[1].strip())

                except ValueError:
                    raise ValueError(
                        f"Page numbers must be integers: {part}"
                    )

                if start < 1 or end > max_pages:
                    raise ValueError(
                        f"Pages must be between 1 and {max_pages}."
                    )

                if start > end:
                    raise ValueError(
                        "Start page cannot be greater than end page."
                    )

                pages.update(
                    range(start - 1, end)
                )

            else:

                try:
                    page = int(part)

                except ValueError:
                    raise ValueError(
                        f"Invalid page number: {part}"
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

    # --------------------------------------------------
    # PDF SPLITTING
    # --------------------------------------------------

    def split_pdf(self):

        input_pdf = self.pdf_path.get()
        output_folder = self.output_dir.get()
        range_string = self.range_entry.get()

        # Validate input
        if not input_pdf or not Path(input_pdf).is_file():
            messagebox.showwarning(
                "Missing PDF",
                "Please select a valid PDF file."
            )
            return

        if not output_folder or not Path(output_folder).is_dir():
            messagebox.showwarning(
                "Missing Output Folder",
                "Please select a valid output folder."
            )
            return

        # Validate page ranges
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

        self.split_button.config(state="disabled")
        self.progress["value"] = 0
        self.status_text.set("Starting PDF extraction...")

        self.root.update_idletasks()

        try:

            reader = PdfReader(input_pdf)

            if reader.is_encrypted:
                raise ValueError(
                    "Cannot process an encrypted PDF."
                )

            writer = PdfWriter()

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

            # Generate output filename
            input_name = Path(input_pdf).stem

            output_path = (
                Path(output_folder)
                / f"{input_name}_split.pdf"
            )

            # Avoid overwriting existing files
            output_path = self.get_unique_output_path(
                output_path
            )

            # Save extracted PDF
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            self.progress["value"] = 100

            self.status_text.set(
                f"Successfully extracted {total_selected} page(s)."
            )

            messagebox.showinfo(
                "Success",
                "PDF created successfully!\n\n"
                f"Pages extracted: {total_selected}\n"
                f"Saved to:\n{output_path}"
            )

        except Exception as error:

            self.progress["value"] = 0

            self.status_text.set(
                "Failed to split PDF."
            )

            messagebox.showerror(
                "Error",
                f"An error occurred while splitting PDF:\n\n{error}"
            )

        finally:
            self.split_button.config(state="normal")

    # --------------------------------------------------
    # OUTPUT FILE HANDLING
    # --------------------------------------------------

    @staticmethod
    def get_unique_output_path(path):
        """
        Prevent overwriting existing output files.

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


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    root = tk.Tk()

    app = PDFSplitterApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
