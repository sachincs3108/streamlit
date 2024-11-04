import streamlit as st
from dcf_calculations import fetch_screener_data

# Right Pane (User Inputs)
st.sidebar.header("DCF Parameters")

symbol = st.sidebar.text_input("Enter NSE/BSE Symbol", "TCS")
# fetch_screener_data(symbol)
my_data=fetch_screener_data(symbol)
print("data fetched:",my_data)

cost_of_capital = st.sidebar.number_input("Cost of Capital (%)", min_value=8.0, max_value=16.0, step=1.0)
roce = st.sidebar.number_input("RoCE (%)", min_value=10.0, max_value=100.0, step=10.0)
growth_rate = st.sidebar.number_input("Growth Rate during High Growth Period (%)", min_value=8.0, max_value=20.0, step=2.0)
high_growth_period = st.sidebar.number_input("High Growth Period (years)", min_value=10.0, max_value=25.0, step=5.0)
fade_period = st.sidebar.number_input("Fade Period (years)", min_value=5.0, max_value=20.0, step=5.0)
terminal_growth_rate = st.sidebar.number_input("Terminal Growth Rate (%)", min_value=0.0, max_value=8.0, step=1.0)

if st.sidebar.button("Calculate"):
    # Call the function to fetch data and compute DCF results
    # Placeholder values for example
    current_pe = my_data['Stock P/E']
    fy23_pe = my_data['FY24 PE']
    roce_5y_median = 22.5
    sales_growth_rates = f"{my_data['TTM:']} (TTM), {my_data['3 Years:']} (3Y), {my_data['5 Years:']} (5Y), {my_data['10 Years:']} (10Y)"
    profit_growth_rates = "12% (TTM), 13% (3Y), 14% (5Y), 16% (10Y)"
    intrinsic_pe = 25
    degree_overvaluation = "10% overvalued"

    # Left Pane (Output Section)
    st.header("Financial Metrics and DCF Results")
    st.write(f"**Current PE**: {current_pe}")
    st.write(f"**FY23 PE**: {fy23_pe}")
    st.write(f"**5-Year Median RoCE**: {roce_5y_median}")
    st.write(f"**Compounded Sales Growth (TTM, 3Y, 5Y, 10Y)**: {sales_growth_rates}")
    st.write(f"**Compounded Profit Growth (TTM, 3Y, 5Y, 10Y)**: {profit_growth_rates}")
    st.write(f"**Calculated Intrinsic PE**: {intrinsic_pe}")
    st.write(f"**Degree of Overvaluation**: {degree_overvaluation}")
