import pandas as pd
from sklearn.metrics import classification_report
from openpyxl import load_workbook

# Define the path to the Excel file
excel_path = "output/sims_x_post_topic_zero_shot.xlsx"

# Read the processed Excel file
df = pd.read_excel(excel_path, sheet_name='model_&_human_based_annotation')

# Define the prediction columns and the ground truth column
prediction_columns = [
    'prediction_mDeBERTa',
    'prediction_facebookbart',
    'prediction_roberta',
    'prediction_multilingual'
]
ground_truth_shahnawaz = 'ground_truth(shahnawaz)'
ground_truth_masba = 'ground_truth(masba)'

# Function to calculate and return classification report as a DataFrame
def get_classification_report(pred_col, true_col):
    y_true = df[true_col].astype(str)  # Convert to string type
    y_pred = df[pred_col].astype(str)  # Convert to string type
    
    report = classification_report(y_true, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    return report_df

# Load the existing workbook
book = load_workbook(excel_path)

# Create a Pandas Excel writer using openpyxl as the engine
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}

    for pred_col in prediction_columns:
        report_df_shahnawaz = get_classification_report(pred_col, ground_truth_shahnawaz)
        report_sheet_name_shahnawaz = f'classification_report_{pred_col}_shahnawaz'
        
        # Write the classification report to a new sheet for Shahnawaz ground truth
        report_df_shahnawaz.to_excel(writer, sheet_name=report_sheet_name_shahnawaz)
        
        # Repeat the process for Masba ground truth
        report_df_masba = get_classification_report(pred_col, ground_truth_masba)
        report_sheet_name_masba = f'classification_report_{pred_col}_masba'
        
        # Write the classification report to a new sheet for Masba ground truth
        report_df_masba.to_excel(writer, sheet_name=report_sheet_name_masba)

    # Save the workbook
    writer.save()

print("Classification reports have been calculated and saved in the Excel file.")
