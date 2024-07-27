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

def standardize_terms(df):
    for col in df.columns:
        mask = df[col].notna() & df[col].astype(str).str.strip() != ""  # Create a mask for non-empty cells
        for main_term, alternatives in term_mapping.items():
            df.loc[mask, col] = df.loc[mask, col].astype(str).str.lower().replace(alternatives, main_term)
    return df


# Streamlit App
st.title('Financial Term Standardizer')

# File Uploader
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file,  
 on_bad_lines='skip')  # Use on_bad_lines

        # Display Original Data
        st.subheader('Original Data')
        st.dataframe(df)

        # Standardize Terms
        standardized_df = standardize_terms(df)

        # Display Standardized Data
        st.subheader('Standardized Data')
        st.dataframe(standardized_df)

        # Download Link
        csv = standardized_df.to_csv(index=False)
        st.download_button(
            label="Download Standardized CSV",
            data=csv,
            file_name='standardized_financials.csv',
            mime='text/csv',
        )
    
    except pd.errors.ParserError as e:
        st.error(f"Error reading CSV: {e}")
