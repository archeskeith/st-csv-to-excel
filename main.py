import streamlit as st
import pandas as pd

def clean_data(df):
    # Remove '\n' and '/n' from each cell in the dataframe
    df = df.replace({'\n': '', '/n': ''}, regex=True)
    return df

def main():
    st.title("CSV Cleaner")

    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Clean the data
        cleaned_df = clean_data(df)
        
        # Display the cleaned dataframe
        st.write("Cleaned Data:")
        st.dataframe(cleaned_df)
        
        # Download link for the cleaned dataframe
        cleaned_csv = cleaned_df.to_csv(index=False)
        st.download_button(
            label="Download Cleaned CSV",
            data=cleaned_csv,
            file_name='cleaned_data.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    main()
