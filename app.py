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
    new_property = st.expander(expander_title)

    with new_property:
        property_name = st.text_input('Property Name', '')
        net_profit = st.number_input('Net Profit', value=0)
        cost_of_investment = st.number_input('Cost of Investment', value=0)
        discount_rate = st.number_input('Discount Rate', value=0.05, min_value=0, max_value=1, step=0.01)
        initial_investment = st.number_input('Initial Investment', value=0)
        net_operating_income = st.number_input('Net Operating Income', value=0)
        market_price_per_share = st.number_input('Market Price per Share', value=0)
        dividends_on_preferred_stock = st.number_input('Dividends on Preferred Stock', value=0)
        avg_outstanding_shares = st.number_input('Average Outstanding Shares', value=0)
        current_market_value = st.number_input('Current Market Value', value=0)

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
            try:
                df_upload = pd.read_csv(uploaded_file)

                # Check if the required columns are present in the uploaded CSV
                required_columns = ['Property', 'Net Profit', 'Cost of Investment', 'Discount Rate',
                                    'Initial Investment', 'Net Operating Income', 'Market Price per Share',
                                    'Dividends on Preferred Stock', 'Average Outstanding Shares', 'Current Market Value']

                if all(col in df_upload.columns for col in required_columns):
                    # Calculate additional metrics
                    df_upload = calculate_additional_metrics(df_upload)

                    # Displaying the uploaded data
                    display_property_data(df_upload, "Uploaded Property Data:")
                else:
                    st.error("Please make sure the uploaded CSV file contains all required columns.")

            except Exception as e:
                st.error(f"An error occurred while processing the uploaded file: {str(e)}")

    # Display the existing data
    if not df.empty:
        display_property_data(df, "Existing Property Data:")

    # Add new property through user input
    df = add_new_property('Add New Property', df)

if __name__ == "__main__":
    main()
