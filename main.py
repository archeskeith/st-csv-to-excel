import streamlit as st
import pandas as pd
import base64
from io import StringIO

# Function to clean the newlines and "/n"
def remove_newline_chars(file_path):
    df = pd.read_csv(file_path, skiprows=2)

    # Clean column names
    df.columns = df.columns.str.replace(r'\n|/n', '', regex=True) 

    # Clean cell values
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'\n|/n', '', regex=True)

    return df

# Streamlit App
st.title("CSV Newline & '/n' Cleaner") 

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    df_cleaned = remove_newline_chars(stringio)

    st.subheader("Cleaned Data:")
    st.dataframe(df_cleaned)

    # Download
    csv = df_cleaned.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_data.csv">Download Cleaned CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
