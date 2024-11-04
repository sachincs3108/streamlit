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

def calculate_intrinsic_pe_and_overvaluation(
    net_profit, current_pe, fy23_pe,
    roce, growth_rate, high_growth_years, fade_years,
    terminal_growth_rate, cost_of_capital, tax_rate=0.25
):
    # Ensure numeric conversion
    try:
        net_profit = float(net_profit.replace(",", ""))
        current_pe = float(current_pe)
        fy23_pe = float(fy23_pe)
        roce = float(roce)
        growth_rate = float(growth_rate)
        high_growth_years = int(high_growth_years)
        fade_years = int(fade_years)
        terminal_growth_rate = float(terminal_growth_rate)
        cost_of_capital = float(cost_of_capital)
        tax_rate = float(tax_rate)
    except ValueError as e:
        print("Error: One or more inputs could not be converted to a number:", e)
        return None, None

    # Constants and Initializations
    intrinsic_pe = 0
    total_pv_fcfs = 0

    # Step 1: Calculate FCFs for High-Growth Period
    for year in range(1, high_growth_years + 1):
        fcf = net_profit * (1 - tax_rate) * (roce - growth_rate) / 100
        pv_fcf = fcf / ((1 + cost_of_capital) ** year)
        total_pv_fcfs += pv_fcf
        net_profit *= (1 + growth_rate / 100)  # Increase for next year's growth

    # Step 2: Calculate FCFs for Fade Period (linearly decreasing growth)
    for year in range(1, fade_years + 1):
        fade_growth_rate = growth_rate - (growth_rate - terminal_growth_rate) * (year / fade_years)
        fcf = net_profit * (1 - tax_rate) * (roce - fade_growth_rate) / 100
        pv_fcf = fcf / ((1 + cost_of_capital) ** (high_growth_years + year))
        total_pv_fcfs += pv_fcf
        net_profit *= (1 + fade_growth_rate / 100)  # Adjust for next year's growth

    # Step 3: Calculate Terminal Value and Discount it
    terminal_value = net_profit * (1 - tax_rate) * (1 + terminal_growth_rate / 100) / (cost_of_capital - terminal_growth_rate)
    pv_terminal_value = terminal_value / ((1 + cost_of_capital) ** (high_growth_years + fade_years))
    total_pv_fcfs += pv_terminal_value

    # Step 4: Calculate Intrinsic PE (PV of FCFs / Net Profit)
    intrinsic_pe = total_pv_fcfs / net_profit

    # Step 5: Calculate Degree of Overvaluation
    reference_pe = min(current_pe, fy23_pe)
    degree_of_overvaluation = (reference_pe / intrinsic_pe) - 1

    return intrinsic_pe, degree_of_overvaluation


intrinsic_pe, overvaluation = calculate_intrinsic_pe_and_overvaluation(
    my_data['fy_24'], my_data['Stock P/E'],my_data['FY24 PE'], roce, growth_rate, high_growth_period,
    fade_period, terminal_growth_rate, cost_of_capital
)

# print("Intrinsic PE:", intrinsic_pe)
# print("Degree of Overvaluation:", overvaluation)


if st.sidebar.button("Calculate"):
    # Call the function to fetch data and compute DCF results
    # Placeholder values for example
    current_pe = my_data['Stock P/E']
    fy23_pe = my_data['FY24 PE']
    roce_5y_median = 22.5
    sales_growth_rates = f"{my_data['Compounded Sales Growth TTM:']} (TTM), {my_data['Compounded Sales Growth 3 Years:']} (3Y), {my_data['Compounded Sales Growth 5 Years:']} (5Y), {my_data['Compounded Sales Growth 10 Years:']} (10Y)"
    profit_growth_rates = f"{my_data['Compounded Profit Growth TTM:']} (TTM), {my_data['Compounded Profit Growth 3 Years:']} (3Y), {my_data['Compounded Profit Growth 5 Years:']} (5Y), {my_data['Compounded Profit Growth 10 Years:']} (10Y)"
    # intrinsic_pe = 25
    # degree_overvaluation = "10% overvalued"

    # Left Pane (Output Section)
    st.header("Financial Metrics and DCF Results")
    st.write(f"**Current PE**: {current_pe}")
    st.write(f"**FY23 PE**: {fy23_pe}")
    st.write(f"**5-Year Median RoCE**: {roce_5y_median}")
    st.write(f"**Compounded Sales Growth (TTM, 3Y, 5Y, 10Y)**: {sales_growth_rates}")
    st.write(f"**Compounded Profit Growth (TTM, 3Y, 5Y, 10Y)**: {profit_growth_rates}")
    st.write(f"**Calculated Intrinsic PE**: {intrinsic_pe}")
    st.write(f"**Degree of Overvaluation**: {overvaluation}")
