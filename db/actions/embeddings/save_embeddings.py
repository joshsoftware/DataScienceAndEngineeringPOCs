from src.embeddings.service import EmbeddingService
from db.index import UserSession


def save_embeddings(data: dict, session: UserSession, org_meta: dict) -> None:
    """
    Process the file to generate embeddings and associate them with the given organization metadata.
    
    :param data: A dictionary containing data like file path
    :param session: A session instance for interacting with the database
    :param org_meta: Organization metadata to associate with the embeddings
    :return: None
    """
    # Step: Call the EmbeddingService to process the file and generate embeddings
    embedding_service = EmbeddingService()
    embedding_service.process_file(data['filePath'], session, org_meta)