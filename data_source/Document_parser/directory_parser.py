'''This method expect path of the directory and load all the files from directory(eg. .txt, .csv, .docs, .xlsx)'''
from langchain_community.document_loaders import DirectoryLoader

def parse_documents(dir_path: str):
    loader = DirectoryLoader(dir_path)
    all_documents = loader.load()
    return all_documents




