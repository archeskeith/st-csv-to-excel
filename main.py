import streamlit as st
import pandas as pd
import base64
from io import StringIO

def clean_and_convert_csv(file_contents):
    """Cleans and converts a CSV file content string into a DataFrame,
       removing newlines and commas within numeric values."""

    headers, rows = final_string_to_csv(file_contents)

    # Handle cases where the first row is not the header
    if len(rows) > 0 and len(rows[0]) == len(headers):
        df_cleaned = pd.DataFrame(rows, columns=headers)
    else:
        # Assume no header row and assign default column names
        df_cleaned = pd.DataFrame(rows)
        headers = [f"Column {i+1}" for i in range(len(df_cleaned.columns))]
        df_cleaned.columns = headers

    # Remove commas and newlines, convert to numeric where possible
    for col in df_cleaned.columns:
        df_cleaned[col] = df_cleaned[col].astype(str).str.replace(r'[,\n]', '', regex=True)
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

    return df_cleaned

# Function to convert a string with '|' and '\n' delimiters into CSV format
def final_string_to_csv(input_string):
    """Converts a string with '|' and '\n' delimiters into CSV format.

    This function removes commas from numeric values, handles newlines, and
    removes newline characters from string values, including those
    within numbers.
    """
    rows = input_string.splitlines()

    # Preprocess rows to remove commas from numeric values and '\n' from strings
    processed_rows = []
    for row in rows:
        columns = row.split("|")
        processed_columns = []
        for col in columns:
            # Remove newlines and forward slashes from strings
            if isinstance(col, str):
                col = col.replace("\n", "").replace("/", "")
            try:
                # Remove commas and convert to integer if possible
                processed_columns.append(int(col.replace(",", "")))
            except ValueError:
                # Keep the cell as a string if conversion fails
                processed_columns.append(col)

        processed_rows.append(processed_columns)

    headers = processed_rows[0]  # Extract headers
    rows = processed_rows[1:]  # Extract data rows

    return headers, rows

# Streamlit App
st.title("CSV Newline Cleaner")
# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded file using StringIO to avoid temporary files
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    file_contents = stringio.read()

    # Clean the CSV data using the function
    df_cleaned = clean_and_convert_csv(file_contents)

    # Display cleaned data
    st.subheader("Cleaned Data:")
    st.dataframe(df_cleaned)

    # Download button
    csv = df_cleaned.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_data.csv">Download Cleaned CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
