import pandas as pd
import replicate
import time
from credentials import replicate_api_key

# Set your Replicate API token
replicate.api_token = replicate_api_key

# Define candidate labels
candidate_labels = [
    "Political", "Business", "Development", "Education", "Sports", 
    "Religion", "Crime", "Election", "Entertainment", "Health", 
    "Accident", "Corruption", "Science-technology"
]

# Function to predict the topic using the Replicate API
def predict_topic(post_text, candidate_labels):
    prompt = f"Classify the following text into one of the categories: {', '.join(candidate_labels)}.\n\nText: {post_text}\n\nCategory:"

    input_data = {
        "prompt": prompt,
        "prompt_template": "system\n\nYou are a helpful assistant\n\nuser\n\n{prompt}\n\nassistant\n\n",
        "presence_penalty": 0,
        "frequency_penalty": 0
    }

    max_retries = 5
    for retry in range(max_retries):
        try:
            for event in replicate.stream(
                "meta/meta-llama-3-8b-instruct",
                input=input_data
            ):
                return event['text'].strip()
        except replicate.exceptions.ReplicateError as e:
            if "free time limit" in e.detail.lower():
                print("Free time limit reached. Please set up billing at https://replicate.com/account/billing#billing to continue using Replicate.")
                return None
            else:
                wait_time = 2 ** retry  # Exponential backoff
                print(f"Error: {e.detail}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
    print("Max retries reached. Unable to get a prediction.")
    return None

# Load the Excel file
input_file = "output/sims_post_topic_zero_shot.xlsx"
sheet_name = "model_&_human_based_annotation"
df = pd.read_excel(input_file, sheet_name=sheet_name)

# Ensure there is a 'post_text' column
if 'post_text' not in df.columns:
    raise ValueError("The input Excel file must contain a 'post_text' column")

# Apply the prediction function to the 'post_text' column
df['topic_label'] = df['post_text'].apply(lambda x: predict_topic(str(x), candidate_labels))

# Save the updated DataFrame to a new Excel file
output_file = "output/sims_post_topic_prediction.xlsx"
df.to_excel(output_file, index=False)

print(f"Topic labeling completed and saved to {output_file}")
m