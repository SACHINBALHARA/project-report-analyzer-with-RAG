from langchain.document_loaders import PyPDFLoader


def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    documents = []
    for page in pages:
        documents.append(
            {
                "text": page.page_content,
                "metadata": {
                    "source": pdf_path,
                    "page": page.metadata.get("page")
                }
            }
        )

    return documents
