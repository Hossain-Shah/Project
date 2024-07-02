import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from huggingface_hub import login
from credentials import hugging_face_token

# Set your Hugging Face token
hf_token = hugging_face_token

# Authenticate using the Hugging Face CLI
login(token=hf_token)

# Model and tokenizer initialization
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=hf_token)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,  # Use mixed precision
    use_auth_token=hf_token,
    device_map="auto",
    offload_folder="offload",  # Offload model parts to disk if possible
)

# Enable gradient checkpointing if supported
model.gradient_checkpointing_enable()

# Function to generate response
def generate_response(post_text):
    messages = [
        {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
        {"role": "user", "content": post_text},
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    # Get eos_token_id
    eos_token_id = tokenizer.eos_token_id
    if eos_token_id is None:
        raise ValueError("The tokenizer does not have an eos_token_id")

    try:
        with torch.no_grad():
            outputs = model.generate(
                input_ids,
                max_new_tokens=256,
                eos_token_id=eos_token_id,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
        response = outputs[0][input_ids.shape[-1]:]
        return tokenizer.decode(response, skip_special_tokens=True)
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()  # Clear cache and retry
        return "Out of memory error while generating response."

# Define the candidate labels
candidate_labels = ["Political", "Business", "Development", "Education", "Sports", "Religion", "Crime", "Election", "Entertainment", "Health", "Accident", "Corruption", "Science-technology"]

# Function to classify response based on the highest matching topic
def classify_response(response_text):
    max_score = float('-inf')
    best_label = None

    for label in candidate_labels:
        prompt = f"The following text is about {label}: {response_text}"
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
            loss = outputs.loss.item()
            score = -loss  # Lower loss means better match, so we use the negative loss as the score

        if score > max_score:
            max_score = score
            best_label = label

    return best_label

# Load the Excel file
input_file = "output/sims_post_topic_zero_shot.xlsx"
sheet_name = "model_&_human_based_annotation"
df = pd.read_excel(input_file, sheet_name=sheet_name)

# Ensure there is a 'post_text' column
if 'post_text' not in df.columns:
    raise ValueError("The input Excel file must contain a 'post_text' column")

# Generate responses and classify them in smaller batches
batch_size = 10  # Adjust batch size as needed to fit in memory
num_batches = (len(df) + batch_size - 1) // batch_size  # Calculate the number of batches

responses = []
predictions = []

for i in range(num_batches):
    batch = df.iloc[i*batch_size:(i+1)*batch_size]
    for post_text in batch['post_text']:
        response = generate_response(post_text)
        responses.append(response)
        prediction = classify_response(response)
        predictions.append(prediction)

df['response'] = responses
df['prediction'] = predictions

# Save the updated DataFrame to a CSV file
output_file = "output/llama_instruct_prediction.csv"
df.to_csv(output_file, index=False)

print(f"Responses and predictions have been generated and saved to {output_file}")
