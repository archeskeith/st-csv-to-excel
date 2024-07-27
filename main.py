import streamlit as st
import pandas as pd
from io import BytesIO

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
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display the uploaded dataframe
        st.write("Uploaded Data:")
        st.dataframe(df)
        
        # Convert the DataFrame to XLSX
        xlsx_data = convert_to_excel(df)
        
        # Download link for the XLSX file
        st.download_button(
            label="Download XLSX",
            data=xlsx_data,
            file_name='converted_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

if __name__ == "__main__":
    main()
