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


def standardize_terms(df, terms_dict):
    """Standardizes terms in the first column of a DataFrame using a dictionary."""
    for main_term, alternatives in terms_dict.items():
        for alt_term in alternatives:
            df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.lower().str.replace(alt_term, main_term, regex=False)
    return df

def main():
    st.title("Financial Term Standardization")

    # Upload CSV File
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Original  
 Data:")
        st.dataframe(df)

        # Standardize Terms
        standardized_df = standardize_terms(df.copy(), financial_terms)
        st.write("Standardized Data:")
        st.dataframe(standardized_df)

        # Download Link for Standardized CSV
        csv = standardized_df.to_csv(index=False)
        st.download_button(
            label="Download Standardized CSV",
            data=csv,
            file_name="standardized_data.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
