import pandas as pd

# Load the Excel file
input_excel_file = "output/sims_post_topic_zero_shot.xlsx"  # Replace with your input Excel file path
sheet_name = "model_&_human_based_annotation"  # Replace with the name of the sheet you want to process

# Read the specific sheet into a DataFrame
df = pd.read_excel(input_excel_file, sheet_name=sheet_name)

# Check if 'post_text' column exists
if 'post_text' in df.columns:
    # Remove rows where 'post_text' column is empty
    df = df[df['post_text'].notna() & df['post_text'].str.strip().astype(bool)]
    
    # Remove duplicate 'post_text' values
    df = df.drop_duplicates(subset='post_text')
else:
    print("The column 'post_text' does not exist in the Excel sheet.")

# Save the updated DataFrame back to the same sheet
with pd.ExcelWriter(input_excel_file, mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Empty and duplicate rows removed and updated Excel file saved.")
