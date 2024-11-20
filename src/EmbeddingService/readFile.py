class ReadFromSource:
  def __init__(self, file_path):
    self.file_path = file_path

  def read_file(self):
    try: 
      with open(self.file_path, "r") as file:
        content = file.read()
        return content
    except FileNotFoundError:
      print("File not Found")
    except IOError:
      print("Something went wrong while reading the file")
