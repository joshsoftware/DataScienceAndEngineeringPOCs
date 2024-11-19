import os
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.preprocessing import normalize

# Check for device compatibility (MPS for macOS or fallback to CPU)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Prompt for queries
query_prompt = (
    "Instruct: Given a web search query, retrieve relevant passages that answer the query.\nQuery: "
)
queries = [
    "What are some ways to reduce stress?",
    "What are the benefits of drinking green tea?",
]
queries = [query_prompt + query for query in queries]

# Document contents without prompts
docs = [
    "There are many effective ways to reduce stress. Some common techniques include deep breathing, meditation, and physical activity. Engaging in hobbies, spending time in nature, and connecting with loved ones can also help alleviate stress. Additionally, setting boundaries, practicing self-care, and learning to say no can prevent stress from building up.",
    "Green tea has been consumed for centuries and is known for its potential health benefits. It contains antioxidants that may help protect the body against damage caused by free radicals. Regular consumption of green tea has been associated with improved heart health, enhanced cognitive function, and a reduced risk of certain types of cancer. The polyphenols in green tea may also have anti-inflammatory and weight loss properties.",
]

# Path to the pre-trained model
model_dir = "../stella_en_1.5B_v5/"

# Vector configuration
vector_dim = 1024
vector_linear_directory = f"2_Dense_{vector_dim}"

# Load model and tokenizer
model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).to(device).eval()
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

# Load the custom linear layer
vector_linear = torch.nn.Linear(
    in_features=model.config.hidden_size, out_features=vector_dim
)
vector_linear_dict = {
    k.replace("linear.", ""): v
    for k, v in torch.load(
        os.path.join(model_dir, f"{vector_linear_directory}/pytorch_model.bin"),
        map_location=device,
    ).items()
}
vector_linear.load_state_dict(vector_linear_dict)
vector_linear.to(device)

def embed_texts(texts, model, tokenizer, vector_linear, device, max_length=512):
    """Helper function to embed texts (queries or documents)."""
    with torch.no_grad():
        input_data = tokenizer(
            texts, padding="longest", truncation=True, max_length=max_length, return_tensors="pt"
        )
        input_data = {k: v.to(device) for k, v in input_data.items()}
        attention_mask = input_data["attention_mask"]
        last_hidden_state = model(**input_data)[0]
        # Masked mean pooling
        last_hidden = last_hidden_state.masked_fill(
            ~attention_mask[..., None].bool(), 0.0
        )
        pooled_embeddings = last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]
        return normalize(vector_linear(pooled_embeddings).cpu().numpy())

# Embed queries and documents
query_vectors = embed_texts(queries, model, tokenizer, vector_linear, device)
docs_vectors = embed_texts(docs, model, tokenizer, vector_linear, device)

print(f"Query vectors shape: {query_vectors.shape}, Document vectors shape: {docs_vectors.shape}")
# (2, 1024) (2, 1024)

# Compute cosine similarity
similarities = query_vectors @ docs_vectors.T
print("Similarities:")
print(similarities)
# Expected output: similarity matrix (2x2)

