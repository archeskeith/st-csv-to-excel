import streamlit as st
import pandas as pd

# Your Dictionary of Terms
term_mapping = {
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

def standardize_csv(uploaded_file):
    df = pd.read_csv(uploaded_file, on_bad_lines='skip')  # Skip bad lines

    # Standardize the first column
    for index, row in df.iterrows():
        term_to_check = row[0].lower()  # Get the term in lowercase
        for main_term, alternatives in financial_terms.items():
            if term_to_check in alternatives:
                df.at[index, 0] = main_term  # Replace with the main term
                break  # Move on to the next row

    return df

# Streamlit App
st.title("CSV Financial Term Standardization")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.subheader("Original Data (Skipping Bad Lines)")
    st.write(pd.read_csv(uploaded_file, on_bad_lines='skip'))

    standardized_df = standardize_csv(uploaded_file)

    st.subheader("Standardized Data (Skipping Bad Lines)")
    st.write(standardized_df)

    
    # Download Link
    csv = standardized_df.to_csv(index=False)
    st.download_button(
        label="Download Standardized CSV",
        data=csv,
        file_name="standardized_financial_data.csv",
        mime="text/csv",
    )
