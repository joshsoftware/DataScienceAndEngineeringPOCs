import os
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.preprocessing import normalize

class CreateEmbeddings:
  def __init__(self, segmented_data):
    self.segmented_data = segmented_data
  
  def generate_embeddings(self):
    # docs do not need any prompts
    docs = [
        "There are many effective ways to reduce stress. Some common techniques include deep breathing, meditation, and physical activity. Engaging in hobbies, spending time in nature, and connecting with loved ones can also help alleviate stress. Additionally, setting boundaries, practicing self-care, and learning to say no can prevent stress from building up.",
        "Green tea has been consumed for centuries and is known for its potential health benefits. It contains antioxidants that may help protect the body against damage caused by free radicals. Regular consumption of green tea has been associated with improved heart health, enhanced cognitive function, and a reduced risk of certain types of cancer. The polyphenols in green tea may also have anti-inflammatory and weight loss properties.",
    ]

    # The path of your model after cloning it
    # @TODO: Need to update this path to env.
    model_dir = "/home/ue/Documents/AI_ML/stella_en_1.5B_v5/"

    vector_dim = 1024
    vector_linear_directory = f"2_Dense_{vector_dim}"
    print('vector_linear_directory: ', vector_linear_directory)
    
    model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).eval()
    print('model: ', model)
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    print('tokenizer: ', tokenizer)
    vector_linear = torch.nn.Linear(in_features=model.config.hidden_size, out_features=vector_dim)
    print('vector_linear: ', vector_linear)
    vector_linear_dict = {
        k.replace("linear.", ""): v for k, v in
        torch.load(os.path.join(model_dir, f"{vector_linear_directory}/pytorch_model.bin")).items()
    }
    vector_linear.load_state_dict(vector_linear_dict)
    vector_linear
    print('vector_linear: ', vector_linear)

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
