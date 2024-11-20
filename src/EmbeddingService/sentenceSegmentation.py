import spacy

class GenerateSentenceSegmentation:
  def __init__(self, file_content):
    self.file_content = file_content

  def generate_sentence_segmentation(self):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(self.file_content)
    print("doc: ", doc)
    newA = []
    s = ""
    for token in doc:
      s = s + token.text + " " if not token.text.__contains__("\n") else s
      if token.is_sent_end and token.text != "\n":
        # print("newLine")
        newA.append(s.strip())
        s = ""
    # print(newA)
    return newA
