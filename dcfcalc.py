import requests
from bs4 import BeautifulSoup

def fetch_screener_data(symbol):
    base_url = "https://www.screener.in/company/"
    consolidated_url = f"{base_url}{symbol}/consolidated/"
    standalone_url = f"{base_url}{symbol}/"

    def parse_data(soup):
        data = {}

        # Current PE (Stock PE)
        pe_ratio_item = soup.find("li", string="Stock P/E")
        if pe_ratio_item:
            pe_ratio_value = pe_ratio_item.find_next("span", class_="number")
            if pe_ratio_value:
                data["Current PE"] = pe_ratio_value.text.strip()

        # Market Cap (for calculating FY23 PE)
        market_cap_item = soup.find("li", string="Market Cap")
        if market_cap_item:
            market_cap_value = market_cap_item.find_next("span", class_="number")
            if market_cap_value:
                data["Market Cap"] = market_cap_value.text.strip()

        # FY23 Net Profit
        net_profit_item = soup.find("li", string="Net Profit")
        if net_profit_item:
            net_profit_value = net_profit_item.find_next("span", class_="number")
            if net_profit_value:
                data["FY23 Net Profit"] = net_profit_value.text.strip()

        # Calculate FY23 PE if Market Cap and FY23 Net Profit are available
        if "Market Cap" in data and "FY23 Net Profit" in data:
            try:
                market_cap = float(data["Market Cap"].replace(",", ""))
                net_profit = float(data["FY23 Net Profit"].replace(",", ""))
                data["FY23 PE"] = market_cap / net_profit
            except ValueError:
                data["FY23 PE"] = "Calculation Error"

        # 5-Year Median RoCE
        roce_item = soup.find("li", string="5 Years RoCE")
        if roce_item:
            roce_value = roce_item.find_next("span", class_="number")
            if roce_value:
                data["5-Year Median RoCE"] = roce_value.text.strip()

        # Compounded Sales and Profit Growth Rates
        growth_items = soup.find_all("li")
        for item in growth_items:
            label = item.find("span", class_="name")
            if label and "Sales Growth" in label.text:
                value = item.find("span", class_="number")
                if value:
                    data["Sales Growth TTM/3/5/10"] = value.text.strip()
            elif label and "Profit Growth" in label.text:
                value = item.find("span", class_="number")
                if value:
                    data["Profit Growth TTM/3/5/10"] = value.text.strip()

        return data

    # Try fetching consolidated data first
    try:
        response = requests.get(consolidated_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            data = parse_data(soup)
            if data:
                return data  # Return if consolidated data was successfully retrieved
    except requests.RequestException as e:
        print(f"Error fetching consolidated data: {e}")

    # Fallback to standalone data if consolidated data is unavailable
    try:
        response = requests.get(standalone_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            data = parse_data(soup)
            if data:
                return data  # Return if standalone data was successfully retrieved
    except requests.RequestException as e:
        print(f"Error fetching standalone data: {e}")

    return None  # Return None if data retrieval failed

# Example usage
symbol = "TCS"
data = fetch_screener_data(symbol)
print(data)
