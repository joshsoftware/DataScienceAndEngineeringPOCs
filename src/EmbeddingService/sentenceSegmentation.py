import spacy

class GenerateSentenceSegmentation:
  def __init__(self, file_content):
    self.file_content = file_content

  def generate_sentence_segmentation(self):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(self.file_content)
    sentenceArray = []
    tempSentence = ""
    for token in doc:
      tempSentence = tempSentence + token.text + " " if not token.text.__contains__("\n") else tempSentence
      if token.is_sent_end and token.text != "\n":
        sentenceArray.append(tempSentence.strip())
        tempSentence = ""
    return sentenceArray
