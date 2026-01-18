from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
    )

    chunks = []

    for doc in documents:
        texts = splitter.split_text(doc["text"])
        for t in texts:
            chunks.append(
                Document(
                    page_content=t,
                    metadata=doc["metadata"],
                )
            )

    return chunks
