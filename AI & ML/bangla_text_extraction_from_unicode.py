import pandas as pd
import re

# Define a regular expression pattern to match Bangla text
bangla_pattern = re.compile(r'[\u0980-\u09FF]+')

def extract_bangla_text(text):
    # Find all Bangla text matches in the text
    bangla_text = bangla_pattern.findall(text)
    # Join the matches into a single string
    return ' '.join(bangla_text)

# Read the CSV file
input_file = "data/sims_data.scraped_data_y.csv"  # Replace with your input CSV file path
df = pd.read_csv(input_file)

# Check if 'post_text' column exists
if 'post_text' in df.columns:
    # Apply the extract_bangla_text function to the 'post_text' column
    df['post_text'] = df['post_text'].apply(lambda x: extract_bangla_text(str(x)))
else:
    print("The column 'post_text' does not exist in the CSV file.")

# Save only the 'post_text' column with the extracted Bangla text to a new CSV file
output_file = "output/sims_y_post_topic_zero_shot.csv"  # Replace with your desired output CSV file path
df[['post_text']].to_csv(output_file, index=False)

print(f"Bangla text extracted and saved to {output_file}")
