import requests
from bs4 import BeautifulSoup


def fetch_screener_data(symbol):
    base_url = "https://www.screener.in/company/"
    consolidated_url = f"{base_url}{symbol}/consolidated/"
    standalone_url = f"{base_url}{symbol}/"

    try:
        response = requests.get(consolidated_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            data = {}

    # Find all list items in the "top-ratios" section
        ratio_items = soup.select("ul#top-ratios li")
    
        for item in ratio_items:
        # Look for the span with class "name" to identify the label
         label = item.find("span", class_="name")
        
         if label and label.text.strip() == "Market Cap":
         # If "Market Cap" label is found, get the span with class "number" for the value
            value = item.find("span", class_="number")
            if value:
                data["Market Cap"] = value.text.strip()
            break  # Exit the loop after finding Market Cap

        # Print extracted data
        if "Market Cap" in data:
            print("Market Cap:", data["Market Cap"])
        else:
            print("Market Cap not found")

        for item in ratio_items:
         # Look for the span with class "name" to identify the label
         label = item.find("span", class_="name")

         if label and label.text.strip() == "Stock P/E":
         # If "Market Cap" label is found, get the span with class "number" for the value
            value = item.find("span", class_="number")
            if value:
                data["Stock P/E"] = value.text.strip()
            break  # Exit the loop after finding Market Cap

        # Print extracted data
        if "Stock P/E" in data:
            print("Stock P/E:", data["Stock P/E"])
        else:
            print("Stock P/E not found")

        section = soup.find('section', id='profit-loss')
        table = section.find('table', class_='data-table responsive-text-nowrap')
        last_row = table.find('tbody').find_all('tr')[-3]
        td_elements = last_row.find_all('td')
        # Retrieve the second-to-last <td> element's text
        if len(td_elements) >= 2:
            FY24 = td_elements[-2].get_text(strip=True)
            print("FY24 value:", FY24)
            data['fy_24'] = FY24
        else:
            print("Not enough <td> elements in the last row to retrieve the second-to-last value.")
        
        if "Market Cap" in data :
            try:
                market_cap = float(data["Market Cap"].replace(",", ""))
                # print("market_cap:",market_cap)
                net_profit = float(data["fy_24"].replace(",", ""))
                data["FY24 PE"] = market_cap / net_profit
                print('FY24 PE: ',data["FY24 PE"])
            except ValueError:
                data["FY24 PE"] = "Not a valid data"

        compounded_sales_growth_table = None
        for table in soup.find_all('table', class_='ranges-table'):
            header = table.find('th', colspan="2")
            if header and header.get_text(strip=True) == "Compounded Sales Growth":
                compounded_sales_growth_table = table
                break

        # Check if the table was found
        if compounded_sales_growth_table:
            compounded_sales_growth = {}
         # Define the periods we're looking for
            periods = ["10 Years:", "5 Years:", "3 Years:", "TTM:"]
            # Loop through each row in the table body
            for row in compounded_sales_growth_table.find_all('tr'):
                cells = row.find_all('td')

                # Check if the row has two cells and the first cell contains one of the periods we're looking for
                if len(cells) == 2 and cells[0].get_text(strip=True) in periods:
                    # Get the period name and its corresponding value
                    period = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)

                    # Store the result in the dictionary
                    compounded_sales_growth[period] = value
                    data[period] = value

            # Output the results
            print("Compounded Sales Growth:")
            for period, value in compounded_sales_growth.items():
                print(f"{period} {value}")

        else:
            print("Table with 'Compounded Sales Growth' header not found.")
        print("data:",data)

    except requests.RequestException as e:
        print(f"Error fetching consolidated data: {e}")

    # If no data could be fetched, return None or an empty dict
    return data


    # Step 2: Fallback to standalone data if consolidated is not available
    try:
        response = requests.get(standalone_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            data = {}

    # Find all list items in the "top-ratios" section
        ratio_items = soup.select("ul#top-ratios li")
    
        for item in ratio_items:
        # Look for the span with class "name" to identify the label
         label = item.find("span", class_="name")
        
         if label and label.text.strip() == "Market Cap":
         # If "Market Cap" label is found, get the span with class "number" for the value
            value = item.find("span", class_="number")
            if value:
                data["Market Cap"] = value.text.strip()
            break  # Exit the loop after finding Market Cap

        # Print extracted data
        if "Market Cap" in data:
            print("Market Cap:", data["Market Cap"])
        else:
            print("Market Cap not found")
        
        for item in ratio_items:
         # Look for the span with class "name" to identify the label
         label = item.find("span", class_="name")
         if label and label.text.strip() == "Stock P/E":
         # If "Market Cap" label is found, get the span with class "number" for the value
            value = item.find("span", class_="number")
            if value:
                data["Stock P/E"] = value.text.strip()
            break  # Exit the loop after finding Market Cap

        # Print extracted data
        if "Stock P/E" in data:
            print("Stock P/E:", data["Stock P/E"])
        else:
            print("Stock P/E not found")

        section = soup.find('section', id='profit-loss')
        table = section.find('table', class_='data-table responsive-text-nowrap')
        last_row = table.find('tbody').find_all('tr')[-3]
        td_elements = last_row.find_all('td')
        # Retrieve the second-to-last <td> element's text
        if len(td_elements) >= 2:
            FY24 = td_elements[-2].get_text(strip=True)
            print("FY24 value:", FY24)
            data['fy_24'] = FY24
        else:
            print("Not enough <td> elements in the last row to retrieve the second-to-last value.")

        if "Market Cap" in data :
            try:
                market_cap = float(data["Market Cap"].replace(",", ""))
                # print("market_cap:",market_cap)
                net_profit = float(data["fy_24"].replace(",", ""))
                data["FY24 PE"] = market_cap / net_profit
                print('FY24 PE: ',data["FY24 PE"])
            except ValueError:
                data["FY24 PE"] = "Not a valid data"

        compounded_sales_growth_table = None
        for table in soup.find_all('table', class_='ranges-table'):
            header = table.find('th', colspan="2")
            if header and header.get_text(strip=True) == "Compounded Sales Growth":
                compounded_sales_growth_table = table
                break

        # Check if the table was found
        if compounded_sales_growth_table:
            compounded_sales_growth = {}
         # Define the periods we're looking for
            periods = ["10 Years:", "5 Years:", "3 Years:", "TTM:"]
            # Loop through each row in the table body
            for row in compounded_sales_growth_table.find_all('tr'):
                cells = row.find_all('td')

                # Check if the row has two cells and the first cell contains one of the periods we're looking for
                if len(cells) == 2 and cells[0].get_text(strip=True) in periods:
                    # Get the period name and its corresponding value
                    period = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)

                    # Store the result in the dictionary
                    compounded_sales_growth[period] = value
                    data[period] = value

            # Output the results
            print("Compounded Sales Growth:")
            for period, value in compounded_sales_growth.items():
                print(f"{period} {value}")

        else:
            print("Table with 'Compounded Sales Growth' header not found.")
        print("data:",data)

    except requests.RequestException as e:
        print(f"Error fetching standalone data: {e}")

    # If no data could be fetched, return None or an empty dict
    return data

# Example usage
symbol = "TCS"
my_data = fetch_screener_data(symbol)
print("data fetched:", my_data)