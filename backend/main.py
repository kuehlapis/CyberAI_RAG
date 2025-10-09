from llm.llm_config import LLMConfig
from repository.chunk_repo import ChunkRepository
from concurrent.futures import ThreadPoolExecutor, as_completed
from repository.pdf_repo import PDFrepository

def main():
    llm_image = LLMConfig()
    llm = LLMConfig(model="gpt-oss-20b:free")
    pdf_repo = PDFrepository()
    pdf = pdf_repo.get_specific_pdf("AICD-Directors-Introduction-to-AI-2025.pdf")
    extractor = ChunkRepository(pdf)
    chunks = extractor.extract_chunks()
    tables, texts, images = extractor.split_chunks(chunks)

    print(texts[0])

    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     if images:
    #         for image in images:
    #             future = executor.submit(llm_image.summarise_image, image)
    #             try:
    #                 image_response = future.result()
    #                 filtered_image = [el for el in image_response if el.lower() != "none"]
    #                 print(filtered_image)
    #             except Exception as e:
    #                 print(f"Error processing image: {e}")
        # if texts:
        #     for text in texts:
        #         future = executor.submit(llm.summarise_function, texts)
        #         try:
        #             text_response = future.result()
        #             print(text_response)
        #         except Exception as e:
        #             print(f"Error processing text: {e}")

        # if tables:
        #     for table in tables:
        #         future = executor.submit(llm.summarise_function, table.metadata.text_as_html)
        #         try:
        #             table_response = future.result()
        #             print(table_response)
        #         except Exception as e:
        #             print(f"Error processing table: {e}")


if __name__ == "__main__":
    main()