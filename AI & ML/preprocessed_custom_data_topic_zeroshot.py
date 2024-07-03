import pandas as pd
from transformers import pipeline
from langdetect import detect, LangDetectException

# Read the CSV file
df = pd.read_csv("data/sims_data.scraped_data_x.csv")

# Initialize an empty list to store all Bangla post text
bangla_posts = []

# Function to detect if text is Bangla
def is_bangla(text):
    try:
        # Check if text is long enough to detect the language
        if len(text.strip()) > 10:  # Adjust length as needed
            return detect(text) == 'bn'
    except LangDetectException:
        return False
    return False

# Iterate over each column containing post text
for col in df.columns:
    if col == "post_text":
        # Append all non-null Bangla post text from the column to the list
        for text in df[col].dropna():
            if is_bangla(text):  # Check if the language is Bangla
                bangla_posts.append(text)

# Create a DataFrame with the concatenated Bangla post text
df = pd.DataFrame({"post_text": bangla_posts})

# Drop duplicate posts
df.drop_duplicates(inplace=True)

# Define models and classifiers
classifier_mDeBERTa = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
classifier_facebookbart = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
classifier_roberta = pipeline("zero-shot-classification", model='cross-encoder/nli-roberta-base')
classifier_multilingual = pipeline("zero-shot-classification", model="MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli")

candidate_labels = ["Political", "Business", "Development", "Education", "Sports", "Religion", "Crime", "Election", "Entertainment", "Health", "Accident", "Corruption", "Science-technology"]

# Define function to predict and return the result
def predict_and_return(post, classifier):
    prediction = classifier(post, candidate_labels, multi_label=False)
    highest_score_label = prediction['labels'][prediction['scores'].index(max(prediction['scores']))]
    return highest_score_label

# Add prediction columns to the DataFrame
df['prediction_mDeBERTa'] = df['post_text'].apply(lambda x: predict_and_return(x, classifier_mDeBERTa))
df['prediction_facebookbart'] = df['post_text'].apply(lambda x: predict_and_return(x, classifier_facebookbart))
df['prediction_roberta'] = df['post_text'].apply(lambda x: predict_and_return(x, classifier_roberta))
df['prediction_multilingual'] = df['post_text'].apply(lambda x: predict_and_return(x, classifier_multilingual))

# Save the posts to a new CSV file
df.to_csv("output/sims_x_post_topic_zero_shot.csv", index=False)
