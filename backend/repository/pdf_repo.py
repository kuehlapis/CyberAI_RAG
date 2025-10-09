from pathlib import Path

class PDFrepository:
    def __init__(self):
        self.base_path = Path("pdfs")
        self.pdfs = []

    def add_pdf(self, pdf: str):
        self.pdfs.append(pdf)

    def get_specific_pdf(self, pdf_name: str = None):
        for pdf in self.base_path.rglob("*.pdf"):
            if pdf_name and pdf.name == pdf_name:
                self.pdfs.append(f"{pdf.parent.name}/{pdf.name}")
                return self.pdfs
            elif not pdf_name:
                print("PDF not in the list")

    def get_year_pdfs(self, year: str = None):
        file_path = self.base_path / year if year else self.base_path
        for pdf in file_path.rglob("*.pdf"):
            self.pdfs.append(f"{year}/{pdf.name}")
        return self.pdfs
    
    def get_all_pdfs(self):
        for pdf in self.base_path.parent.rglob("*.pdf"):
            self.pdfs.append(f"{pdf.parent.name}/{pdf.name}")
        return self.pdfs

if __name__ == "__main__":
    repo = PDFrepository()
    pdfs = repo.get_all_pdfs()
    print(pdfs)
