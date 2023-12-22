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
    st.dataframe(df)

def add_new_property(expander_title, df):
    new_property_expander = st.expander(expander_title)

    with new_property_expander:
        property_name = st.text_input('Property Name', '').strip()

        # Validate and get numeric inputs
        numeric_input = lambda label, default_value=0, min_value=0: st.number_input(label, value=default_value, min_value=min_value)

        net_profit = numeric_input('Net Profit')
        cost_of_investment = numeric_input('Cost of Investment')
        discount_rate = numeric_input('Discount Rate', 0.05, 0, 1, 0.01)
        initial_investment = numeric_input('Initial Investment')
        net_operating_income = numeric_input('Net Operating Income')
        market_price_per_share = numeric_input('Market Price per Share')
        dividends_on_preferred_stock = numeric_input('Dividends on Preferred Stock')
        avg_outstanding_shares = numeric_input('Average Outstanding Shares')
        current_market_value = numeric_input('Current Market Value')

        if st.button('Add Property'):
            new_data = {
                'Property': property_name,
                'Net Profit': net_profit,
                'Cost of Investment': cost_of_investment,
                'Discount Rate': discount_rate,
                'Initial Investment': initial_investment,
                'Net Operating Income': net_operating_income,
                'Market Price per Share': market_price_per_share,
                'Dividends on Preferred Stock': dividends_on_preferred_stock,
                'Average Outstanding Shares': avg_outstanding_shares,
                'Current Market Value': current_market_value,
            }

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

        if set(required_columns).issubset(df_upload.columns):
            # Validate numeric columns in the uploaded CSV
            numeric_columns = df_upload.select_dtypes(include='number').columns
            if not numeric_columns.empty:
                # Calculate additional metrics
                df_upload = calculate_additional_metrics(df_upload)

                # Displaying the uploaded data
                display_property_data(df_upload, "Uploaded Property Data:")
            else:
                st.error("No numeric columns found in the uploaded CSV.")
        else:
            st.error(f"Please make sure the uploaded CSV file contains all required columns: {', '.join(required_columns)}.")

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
