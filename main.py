import streamlit as st
import re
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

def standardize_first_column(df, terms_dict):
    """Standardizes terms in the first column of a DataFrame using a dictionary."""
    first_column_values = df.iloc[:, 0].astype(str).str.lower()

    for main_term, alternatives in terms_dict.items():
        if alternatives:  # Only process if there are alternatives
            pattern = '|'.join(map(re.escape, alternatives))  # Create a regex pattern
            first_column_values = first_column_values.str.replace(pattern, main_term, regex=True)

    df.iloc[:, 0] = first_column_values
    return df


def main():
    st.title("Financial Term Standardization (First Column)")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            # Read CSV with header starting from the third row
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            df = pd.read_csv(stringio, on_bad_lines='skip', header=2)

            # Remove trailing newline characters from column names
            df.columns = df.columns.str.rstrip('\n')

            st.write("Original Data:")
            st.dataframe(df)

            # Check and Clean numeric columns
            numeric_columns = ['2020', '2019']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.replace(r'[,()]', '', regex=True)
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            # Standardize the first column
            standardized_df = standardize_first_column(df.copy(), financial_terms)

            st.write("Standardized Unique Values:")
            st.write(standardized_df.iloc[:, 0].unique())

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
            st.write("Please check your CSV file for inconsistent column counts or invalid characters.")

if __name__ == "__main__":
    main()
