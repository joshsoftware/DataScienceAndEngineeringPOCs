import os
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.preprocessing import normalize
from dotenv import load_dotenv

load_dotenv()

class CreateEmbeddings:
  def __init__(self, segmented_data):
    self.segmented_data = segmented_data
  
  def generate_embeddings(self):
    # The path of your model after cloning it
    MODEL_DIR = os.getenv('MODEL_DIR')
    VECTOR_DIM = int(os.getenv('VECTOR_DIM'))
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    vector_linear_directory = f"2_Dense_{VECTOR_DIM}"

    model = AutoModel.from_pretrained(MODEL_DIR, trust_remote_code=True).eval()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
    vector_linear = torch.nn.Linear(in_features=model.config.hidden_size, out_features=VECTOR_DIM)
    vector_linear_dict = {
        k.replace("linear.", ""): v for k, v in
        torch.load(os.path.join(MODEL_DIR, f"{vector_linear_directory}/pytorch_model.bin"), map_location=torch.device(DEVICE)).items()
    }
    vector_linear.load_state_dict(vector_linear_dict)
    vector_linear

    # Embed the documents
    with torch.no_grad():
        input_data = tokenizer(self.segmented_data, padding="longest", truncation=True, max_length=512, return_tensors="pt")
        input_data = {k: v for k, v in input_data.items()}
        attention_mask = input_data["attention_mask"]
        last_hidden_state = model(**input_data)[0]
        last_hidden = last_hidden_state.masked_fill(~attention_mask[..., None].bool(), 0.0)
        docs_vectors = last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
        docs_vectors = normalize(vector_linear(docs_vectors).cpu().numpy())

    print(docs_vectors.shape)
