import streamlit as st
import pandas as pd
from io import BytesIO

def clean_data(df):
    # Remove '\n' and '/n' from each cell in the dataframe
    df = df.replace({'\n': '', '/n': ''}, regex=True)
    return df

def convert_to_excel(df):
    # Create a BytesIO buffer to save the Excel file
    output = BytesIO()
    # Save the DataFrame to the buffer
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def main():
    st.title("CSV to XLSX Converter")

    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file, on_bad_lines='skip')
            
            # Clean the data
            cleaned_df = clean_data(df)
            
            # Display the cleaned dataframe
            st.write("Cleaned Data:")
            st.dataframe(cleaned_df)
            
            # Convert the DataFrame to XLSX
            xlsx_data = convert_to_excel(cleaned_df)
            
            # Download link for the XLSX file
            st.download_button(
                label="Download XLSX",
                data=xlsx_data,
                file_name='converted_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")

if __name__ == "__main__":
    main()
