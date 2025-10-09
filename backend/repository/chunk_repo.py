import os
from pathlib import Path
import base64
from IPython.display import display, Image
from unstructured.partition.pdf import partition_pdf
from repository.pdf_repo import PDFrepository

pdf_repo = PDFrepository()

class ChunkRepository:
    def __init__(self, file_name: str):
        self.file_path = Path(file_name)

    def extract_chunks(self):
        if not self.file_path or not os.path.exists(self.file_path):
            raise FileNotFoundError("File path is not set or the file does not exist.")
        
        chunks = partition_pdf(
            filename=self.file_path,
            infer_table_structure=True,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000)
        return chunks
    
    @staticmethod
    def split_chunks(chunks):
        tables = []
        texts = []
        images = []

        for chunk in chunks:
            if "Table" in str(type(chunk)):
                tables.append(chunk)

            if "CompositeElement" in str(type(chunk)): 
                chunk_els = chunk.metadata.orig_elements               
                for el in chunk_els:
                    if "Image" in str(type(el)):
                        images.append(el.metadata.image_base64)
                    else:
                        texts.append(chunk)
        return tables, texts, images

    @staticmethod
    def save_image(base64_code):
        image_data = base64.b64decode(base64_code)
        with open("output_image.png", "wb") as f:
            f.write(image_data)


if __name__ == "__main__":
    extractor = ChunkFunctions("2025/AICD-Directors-Introduction-to-AI-2025.pdf")
    chunks = extractor.extract_chunks()
    tables, texts, images = extractor.split_chunks(chunks)
    extractor.save_image(images[0])


    