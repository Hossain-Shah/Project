import pandas as pd

# Read the processed CSV file
df = pd.read_csv("output/sims_x_post_topic_zero_shot.csv")

# Initialize a dictionary to store counts for each label
label_counts = {
    "Political": 0,
    "Business": 0,
    "Development": 0,
    "Education": 0,
    "Sports": 0,
    "Religion": 0,
    "Crime": 0,
    "Election": 0,
    "Entertainment": 0,
    "Health": 0,
    "Accident": 0,
    "Corruption": 0,
    "Science-technology": 0
}

# List of prediction columns
prediction_columns = [
    'prediction_mDeBERTa',
    'prediction_facebookbart',
    'prediction_roberta',
    'prediction_multilingual'
]

# Count occurrences of each label in prediction columns
for col in prediction_columns:
    for label in label_counts.keys():
        label_counts[label] += df[col].value_counts().get(label, 0)

# Print the counts for each label
for label, count in label_counts.items():
    print(f"{label}: {count}")

# Optionally, save the counts to a CSV file
counts_df = pd.DataFrame(list(label_counts.items()), columns=['Label', 'Count'])
counts_df.to_csv("output/label_counts.csv", index=False)
