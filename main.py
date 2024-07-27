import streamlit as st
import pandas as pd
import base64
from io import StringIO

# Function to clean the newlines
def remove_newline_chars(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, skiprows=2)

    # Remove newline characters from column names
    df.columns = df.columns.str.replace('\n', '', regex=False)

    # Remove newline characters and '/n' from all column values
    for column in df.columns:
        df[column] = df[column].astype(str).str.replace(r'\n|/n', '', regex=True)

    return df

# Streamlit App
st.title("CSV Newline Cleaner")

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded file using StringIO to avoid temporary files
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # Clean the CSV data using the function
    df_cleaned = remove_newline_chars(stringio)

    # Display cleaned data
    st.subheader("Cleaned Data:")
    st.dataframe(df_cleaned)

    # Download button
    csv = df_cleaned.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_data.csv">Download Cleaned CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
