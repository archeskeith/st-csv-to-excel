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

# Function to standardize column names based on the mapping
def standardize_columns(df, mapping):
    # Reverse the mapping for easier lookup
    reverse_mapping = {}
    for main_term, alternatives in mapping.items():
        for alt in alternatives:
            reverse_mapping[alt.lower()] = main_term.lower()

    # Match and replace column names
    df.columns = [
        reverse_mapping.get(col.lower(), col)  # Use main term if found, else keep original
        for col in df.columns
    ]
    return df

# Streamlit App
st.title("CSV Column Standardizer")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except pd.errors.ParserError as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()
    # Display original columns
    st.subheader("Original Columns:")
    st.write(df.columns)

    # Standardize columns
    df = standardize_columns(df, term_mapping)

    # Display standardized columns
    st.subheader("Standardized Columns:")
    st.write(df.columns)

    # Download Link (using CSV string to avoid temporary files)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Standardized CSV",
        data=csv,
        file_name="standardized.csv",
        mime="text/csv",
    )
