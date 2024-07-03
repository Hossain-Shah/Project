import openai
import pandas as pd
import time
import logging
from credentials import openai_api_key

# Set your OpenAI API key
openai.api_key = openai_api_key

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define candidate labels
candidate_labels = ["Political", "Business", "Development", "Education", "Sports", "Religion", "Crime", "Election", "Entertainment", "Health", "Accident", "Corruption", "Science-technology"]

def predict_topic(post_text, candidate_labels):
    prompt = f"Classify the following text into one of the categories: {', '.join(candidate_labels)}.\n\nText: {post_text}\n\nCategory:"

    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",  # Use the GPT-3.5 model
                prompt=prompt,
                max_tokens=20,  # Adjust based on expected length of the label
                temperature=0  # Lower temperature to make output more deterministic
            )
            prediction = response.choices[0].text.strip()
            logging.info(f"Predicted topic: {prediction}")
            print(f"Predicted topic for '{post_text}': {prediction}")
            return prediction
        except openai.error.RateLimitError as e:
            retry_count += 1
            wait_time = 2 ** retry_count  # Exponential backoff
            logging.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break
    
    return None  # Return None if unable to get a response after retries

# Read the CSV file
input_file = "output/sims_post_topic_gpt_gemini.csv"  # Replace with your input CSV file path
df = pd.read_csv(input_file)

# Check if 'post_text' column exists
if 'post_text' in df.columns:
    # Apply the prediction function to the 'post_text' column
    df['topic_label'] = df['post_text'].apply(lambda x: predict_topic(str(x), candidate_labels))
else:
    logging.error("The column 'post_text' does not exist in the CSV file.")
    print("The column 'post_text' does not exist in the CSV file.")

# Save the result to a new CSV file
output_file = "output/sims_post_topic_gpt_gemini_result.csv"  # Replace with your desired output CSV file path
df.to_csv(output_file, index=False)

logging.info(f"Topic labeling completed and saved to {output_file}")
print(f"Topic labeling completed and saved to {output_file}")
