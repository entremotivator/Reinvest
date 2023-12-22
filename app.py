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

# Example data for 10 properties
data = {
    'Property': ['Property 1', 'Property 2', 'Property 3', 'Property 4', 'Property 5', 'Property 6', 'Property 7', 'Property 8', 'Property 9', 'Property 10'],
    'Net Profit': [100000, 80000, 120000, 90000, 110000, 95000, 105000, 88000, 115000, 100000],
    'Cost of Investment': [500000, 600000, 450000, 550000, 480000, 520000, 490000, 610000, 470000, 500000],
    'Discount Rate': [0.05, 0.06, 0.04, 0.05, 0.03, 0.07, 0.04, 0.06, 0.05, 0.05],
    'Initial Investment': [450000, 500000, 400000, 480000, 420000, 460000, 430000, 520000, 390000, 450000],
    'Net Operating Income': [80000, 75000, 90000, 82000, 88000, 83000, 86000, 74000, 91000, 80000],
    'Market Price per Share': [50, 60, 45, 55, 48, 52, 49, 61, 47, 50],
    'Dividends on Preferred Stock': [5000, 6000, 4500, 5500, 4800, 5200, 4900, 6100, 4700, 5000],
    'Average Outstanding Shares': [20000, 18000, 22000, 19000, 21000, 20000, 20500, 17500, 22500, 20000],
    'Current Market Value': [600000, 550000, 620000, 580000, 590000, 610000, 570000, 540000, 630000, 600000],
}

df = pd.DataFrame(data)

# Calculate additional metrics
df = calculate_additional_metrics(df)

# Streamlit app
st.title('Property Investment Analysis')

# Displaying the data
st.dataframe(df)

# Add new property through user input
new_property = st.beta_expander('Add New Property')

with new_property:
    property_name = st.text_input('Property Name', '')
    net_profit = st.number_input('Net Profit', value=0)
    cost_of_investment = st.number_input('Cost of Investment', value=0)
    discount_rate = st.number_input('Discount Rate', value=0.05)
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
st.dataframe(df)
