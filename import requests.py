import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = 'https://durbarsquareuk.co.uk/menu/'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all menu items
menu_items = soup.find_all('div', class_='menu-item')

# Initialize lists to store the extracted information
menu_names = []
menu_item_names = []
descriptions = []
prices = []
photos = []
photo_available = []

# Extract information for each menu item
for item in menu_items:
    # Extract menu name
    menu_name = item.find_previous('h3', class_='title').text.strip()
    menu_names.append(menu_name)
    
    menu_item_name = item.find('h5').text.strip()
    menu_item_names.append(menu_item_name)
    
    # Extract description
    description = item.find('small').text.strip()
    descriptions.append(description)
    
    # Extract price
    price = item.find('p', class_='price').text.strip()
    prices.append(price)
    
    # Check if photo is available
    photo = item.find('img')
    if photo and photo['src'] != '':
        photo_url = photo['src']
        photo_available.append('yes')
    else:
        photo_url = 'Not available'
        photo_available.append('no')
    photos.append(photo_url)

# Create a pandas DataFrame to store the extracted information
data = {
    'Menu Name': menu_names,
    'Menu Item Name': menu_item_names,
    'Description': descriptions,
    'Price': prices,
    'Photo': photos,
    'Photo Available': photo_available
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('menu_data.xlsx', index=False)
