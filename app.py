import streamlit as st
import pandas as pd

def calculate_additional_metrics(df):
    df['ROI'] = (df['Net Profit'] / df['Cost of Investment']) * 100
    df['NPV'] = df.apply(lambda row: sum(row['Net Operating Income'] / (1 + row['Discount Rate'])**t for t in range(1, 6)) - row['Initial Investment'], axis=1)
    df['IRR'] = df.apply(lambda row: round(100 * (1 + row['Discount Rate']) ** 2, 2), axis=1)
    df['Cash Flow'] = df['Net Profit'] - df['Initial Investment']
    df['Debt-to-Equity Ratio'] = df['Cost of Investment'] / df['Net Profit']
    df['EPS'] = (df['Net Profit'] - df['Dividends on Preferred Stock']) / df['Average Outstanding Shares']
    df['P/E Ratio'] = df['Market Price per Share'] / df['EPS']
    df['Cap Rate'] = df['Net Operating Income'] / df['Current Market Value']
    return df

def display_property_data(df, title):
    st.subheader(title)
    st.dataframe(df.style.format({
        'Discount Rate': "{:.2%}",
        'ROI': "{:.2f}%",
        'NPV': "${:,.2f}",
        'Cash Flow': "${:,.2f}",
        'IRR': "{:.2f}%",
        'Debt-to-Equity Ratio': "{:.2f}",
        'EPS': "${:,.2f}",
        'P/E Ratio': "{:.2f}",
        'Cap Rate': "{:.2%}"
    }))

def add_new_property(expander_title, df):
    new_property_expander = st.expander(expander_title)

    with new_property_expander:
        property_name = st.text_input('Property Name', '').strip()

        st.subheader("Enter Financial Details:")
        financial_details = {
            'Net Profit': st.number_input('Net Profit', min_value=0),
            'Cost of Investment': st.number_input('Cost of Investment', min_value=0),
            'Discount Rate': st.slider('Discount Rate', min_value=0.01, max_value=1.0, value=0.05, step=0.01),
            'Initial Investment': st.number_input('Initial Investment', min_value=0),
            'Net Operating Income': st.number_input('Net Operating Income', min_value=0),
            'Market Price per Share': st.number_input('Market Price per Share', min_value=0),
            'Dividends on Preferred Stock': st.number_input('Dividends on Preferred Stock', min_value=0),
            'Average Outstanding Shares': st.number_input('Average Outstanding Shares', min_value=0),
            'Current Market Value': st.number_input('Current Market Value', min_value=0)
        }

        if st.button('Add Property'):
            new_data = {'Property': property_name, **financial_details}
            df = df.append(new_data, ignore_index=True)
            df = calculate_additional_metrics(df)

            # Displaying the updated data
            display_property_data(df, "Updated Property Data:")

    return df

def validate_and_display_uploaded_data(uploaded_file):
    try:
        df_upload = pd.read_csv(uploaded_file)

        # Validate columns in the uploaded CSV
        required_columns = ['Property', 'Net Profit', 'Cost of Investment', 'Discount Rate',
                            'Initial Investment', 'Net Operating Income', 'Market Price per Share',
                            'Dividends on Preferred Stock', 'Average Outstanding Shares', 'Current Market Value']

        missing_columns = set(required_columns) - set(df_upload.columns)

        if not missing_columns:
            # Calculate additional metrics
            df_upload = calculate_additional_metrics(df_upload)

            # Displaying the uploaded data
            display_property_data(df_upload, "Uploaded Property Data:")
        else:
            st.error(f"Please make sure the uploaded CSV file contains all required columns: {', '.join(missing_columns)}.")

    except Exception as e:
        st.error(f"An error occurred while processing the uploaded file: {str(e)}")

def main():
    # Streamlit app settings
    st.set_page_config(
        page_title="Property Investment Analysis",
        page_icon=":house:",
        layout="wide"
    )

    # Sidebar
    st.sidebar.title("Options")
    add_property_option = st.sidebar.radio("Add Property:", ("Manually", "Upload CSV"))

    # Main content
    st.title('Property Investment Analysis')

    # Initialize DataFrame
    df = pd.DataFrame()

    # Option to add new property through user input
    if add_property_option == "Manually":
        df = add_new_property('Add New Property', df)
    elif add_property_option == "Upload CSV":
        st.subheader("Upload CSV file with property data:")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file is not None:
            validate_and_display_uploaded_data(uploaded_file)

    # Display the existing data
    if not df.empty:
        display_property_data(df, "Existing Property Data:")

    # Add new property through user input
    df = add_new_property('Add New Property', df)

if __name__ == "__main__":
    main()
