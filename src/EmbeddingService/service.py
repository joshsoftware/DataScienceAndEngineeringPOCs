from readFile import ReadFromSource
from sentenceSegmentation import GenerateSentenceSegmentation
from createEmbeddings import CreateEmbeddings

class RAG:
  def __init__(self, file_path):
    self.file_path = file_path
    self.file_content = ""
    self.sengemented_data = []

  def run_RAG(self):
    """Start Reading the file."""
    readFile = ReadFromSource(self.file_path)
    self.file_content = readFile.read_file()
    
    """Performing sentence segmentation."""
    segmentation = GenerateSentenceSegmentation(self.file_content)
    self.segmented_data = segmentation.generate_sentence_segmentation()
    print(self.segmented_data)
    print(len(self.segmented_data))

    # Create Embaddings
    embeddings = CreateEmbeddings(self.segmented_data)
    embeddings.generate_embeddings()
    
    # insert embedding into PGVector

# RAG()
if __name__ == '__main__':
  rag = RAG("/home/ue/Documents/AI_ML/practice/text.txt")
  rag.run_RAG()