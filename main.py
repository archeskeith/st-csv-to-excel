import streamlit as st

import pandas as pd

import io


# Your Dictionary of Terms

financial_terms = {

   'total interest bearing liabilities or financial debt': ['financial debt', 'total liabilities'],

   'total tangible net worth (equity)': ['total shareholder\'s equity', 'total stockholder\'s equity', 'total equity'],

   'total assets': [],

   'current assets': ['total current assets'],

   'current liabilities': ['total current liabilities'],

   'cash and easily marketable securities': ['cash', 'cash and cash equivalents'],

   'intangible asset': [],

   'short-term debt': ['loans payable - current'],

   'total accounts receivable': ['receivables', 'trade and other receivables'],

   'accounts payable': ['trade payables', 'trade and other payables'],

   'inventory': [],

   'cost of services': ['cost of sales', 'cost of goods', 'cost of goods/cost of services', 'direct costs'],

   'operating expenses': ['operating costs'],

   'earnings before interest and tax': ['operating income', 'earnings before interest and tax (ebit)', 'ebit',

                                       'net income from operations', 'profit before tax', 'income before changes in working capital'],

   'interest expense': [],

   'gross profit': ['gross income'],

   'total revenue': ['gross revenue', 'total sales', 'gross sales', 'revenue', 'service revenues'],

   'net profit after tax': ['net income after tax', 'npat', 'net income', 'net earnings', 'net income (loss) after tax', 'profit for the year'],

   'earnings before interest tax depreciation amortization': ['income before changes in working capital'],

   'operating cash flow': ['ocf', 'net cash provided by operating activities or cash flow from operations',

                          'net cash used in operating activities or cash flow from operations',

                          'net cash flows provided by/(used from) from investing activities',

                          'net cash provided by operating activities',

                          'net cash provided by/(used from) from investing activities',

                          'net cash provided by/(used in) operating activities']

}




def standardize_first_column(df, terms_dict, has_header=True):

   """Standardizes terms in the first column of a DataFrame using a dictionary."""

   if not has_header:

       df.columns = df.iloc[0] # Use first row as headers

       df = df.iloc[1:].copy() # Remove the first row from data


   first_column_values = df.iloc[:, 0].astype(str).str.lower()


   for main_term, alternatives in terms_dict.items():

       for alt_term in alternatives:

           df.iloc[:, 0] = first_column_values.str.replace(alt_term, main_term, regex=False)

   return df


def main():

   st.title("Financial Term Standardization (First Column)")


   uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

   if uploaded_file is not None:

       try:

           # Check if the file has headers

           has_header = st.checkbox("Does the CSV have a header row?", value=True)

           df = pd.read_csv(uploaded_file, on_bad_lines='skip', header=0 if has_header else None)


           st.write("Original Data:")

           st.dataframe(df)


           standardized_df = standardize_first_column(df.copy(), financial_terms, has_header)

           st.write("Standardized Data:")

           st.dataframe(standardized_df)


           csv = standardized_df.to_csv(index=False)

           st.download_button(

               label="Download Standardized CSV",

               data=csv,

               file_name="standardized_data.csv",

               mime="text/csv",

           )


       except pd.errors.ParserError as e:

           st.error(f"Error reading CSV: {e}")

           st.write("Please check your CSV file for inconsistent column counts.")


if __name__ == "__main__":

   main()
