import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os

class PDFSplitterApp:
    def __init__(self, root):
        """
        Initialize the main application window and variables.
        """
        self.root = root
        self.root.title("PDF Splitter")
        self.root.geometry("520x400")
        self.root.resizable(False, False)
        
        # Application variables
        self.pdf_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.total_pages = tk.IntVar(value=0)

        # Setup the User Interface
        self.setup_ui()

    def setup_ui(self):
        """
        Create and arrange the widgets for the application.
        """
        # Title Label
        title_label = tk.Label(self.root, text="Simple PDF Splitter", font=("Arial", 16, "bold"))
        title_label.pack(pady=15)

        # --- Frame for PDF file selection ---
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(file_frame, text="Select PDF:").pack(anchor="w")
        
        file_input_frame = tk.Frame(file_frame)
        file_input_frame.pack(fill="x", pady=5)
        
        # Entry to display selected file path (readonly)
        tk.Entry(file_input_frame, textvariable=self.pdf_path, state="readonly", width=45).pack(side="left", padx=(0, 10))
        # Browse button
        tk.Button(file_input_frame, text="Browse PDF", command=self.browse_pdf).pack(side="left")

        # Label to display the total number of pages in the selected PDF
        self.info_label = tk.Label(file_frame, text="Total Pages: 0", fg="gray")
        self.info_label.pack(anchor="w")

        # --- Frame for Page Ranges input ---
        range_frame = tk.Frame(self.root)
        range_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(range_frame, text="Pages to extract (e.g., 1-3, 5, 8-10):").pack(anchor="w")
        self.range_entry = tk.Entry(range_frame, width=58)
        self.range_entry.pack(pady=5, anchor="w")

        # --- Frame for output folder selection ---
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(output_frame, text="Output Folder:").pack(anchor="w")
        
        output_input_frame = tk.Frame(output_frame)
        output_input_frame.pack(fill="x", pady=5)
        
        # Entry to display selected output folder path (readonly)
        tk.Entry(output_input_frame, textvariable=self.output_dir, state="readonly", width=45).pack(side="left", padx=(0, 10))
        # Browse button
        tk.Button(output_input_frame, text="Browse Folder", command=self.browse_output_folder).pack(side="left")

        # --- Split Button ---
        split_btn = tk.Button(self.root, text="Split PDF", command=self.split_pdf, 
                              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15)
        split_btn.pack(pady=20)

    def browse_pdf(self):
        """
        Open a file dialog to select a PDF file.
        Updates the path variable and reads the PDF to get total pages.
        """
        file_path = filedialog.askopenfilename(
            title="Select a PDF File",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.pdf_path.set(file_path)
            self.update_pdf_info(file_path)

    def browse_output_folder(self):
        """
        Open a dialog to select the folder where the output will be saved.
        """
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_dir.set(folder_path)

    def update_pdf_info(self, file_path):
        """
        Reads the selected PDF to extract basic info like the number of pages.
        """
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                self.total_pages.set(total_pages)
                self.info_label.config(text=f"Total Pages: {total_pages}")
        except Exception as e:
            # Show an error if the file is invalid or corrupted
            messagebox.showerror("Error", f"Failed to read PDF file:\n{e}")
            self.pdf_path.set("")
            self.total_pages.set(0)
            self.info_label.config(text="Total Pages: 0")

    def parse_page_ranges(self, range_string, max_pages):
        """
        Parses a string like "1-3,5,8-10" into a sorted list of unique 0-indexed page numbers.
        Validates the pages against the max_pages limit.
        """
        pages = set()
        # Remove any spaces and split by comma
        parts = range_string.replace(" ", "").split(",")
        
        for part in parts:
            if not part:
                continue
            
            # If part contains a hyphen, it's a range (e.g., "1-3")
            if "-" in part:
                bounds = part.split("-")
                if len(bounds) != 2:
                    raise ValueError(f"Invalid range format: {part}")
                
                start_str, end_str = bounds
                
                try:
                    start = int(start_str)
                    end = int(end_str)
                except ValueError:
                    raise ValueError(f"Page numbers must be integers: {part}")
                
                if start > end:
                    raise ValueError(f"Start page cannot be greater than end page: {part}")
                if start < 1 or end > max_pages:
                    raise ValueError(f"Page numbers must be between 1 and {max_pages}: {part}")
                    
                # Add all pages in the range (inclusive)
                # Note: Subtract 1 because PyPDF2 pages are 0-indexed
                for p in range(start, end + 1):
                    pages.add(p - 1)
            else:
                # Single page number
                try:
                    p = int(part)
                except ValueError:
                    raise ValueError(f"Page numbers must be integers: {part}")
                    
                if p < 1 or p > max_pages:
                    raise ValueError(f"Page numbers must be between 1 and {max_pages}: {p}")
                
                # Note: Subtract 1 because PyPDF2 pages are 0-indexed
                pages.add(p - 1)
                
        if not pages:
            raise ValueError("No valid pages specified.")
            
        return sorted(list(pages))

    def split_pdf(self):
        """
        Main function to split the PDF based on the parsed ranges and save to the output folder.
        """
        input_pdf = self.pdf_path.get()
        output_folder = self.output_dir.get()
        range_str = self.range_entry.get()

        # Input Validation
        if not input_pdf:
            messagebox.showwarning("Warning", "Please select a PDF file first.")
            return
        if not output_folder:
            messagebox.showwarning("Warning", "Please select an output folder.")
            return
        if not range_str:
            messagebox.showwarning("Warning", "Please enter page ranges to extract.")
            return

        try:
            # Parse and validate the page ranges entered by the user
            pages_to_extract = self.parse_page_ranges(range_str, self.total_pages.get())
        except ValueError as e:
            # Show specific parsing/validation error
            messagebox.showerror("Invalid Input", str(e))
            return

        try:
            # Perform the PDF splitting
            with open(input_pdf, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()

                # Add selected pages to the writer
                for page_num in pages_to_extract:
                    writer.add_page(reader.pages[page_num])

                # Define the final output path
                output_path = os.path.join(output_folder, "split_output.pdf")
                
                # Write the new PDF to the disk
                with open(output_path, "wb") as out_file:
                    writer.write(out_file)

            # Show success message
            messagebox.showinfo("Success", f"PDF successfully split and saved to:\n{output_path}")

        except Exception as e:
            # Catch any unexpected errors during PDF processing or writing
            messagebox.showerror("Error", f"An error occurred while splitting the PDF:\n{e}")

if __name__ == "__main__":
    # Create the root Tkinter window and start the app
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
