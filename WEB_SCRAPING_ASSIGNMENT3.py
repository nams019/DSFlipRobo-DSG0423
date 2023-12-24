#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Q1
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def search_amazon_products(product_name):
    
    driver = webdriver.Chrome()  
    driver.get("https://www.amazon.in")

    search_box = driver.find_element("id", "twotabsearchtextbox")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)  

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    product_listings = soup.find_all("div", class_="s-result-item")

    for listing in product_listings:
        product_title = listing.find("h2")
        if product_title:
            print(product_title.text.strip())

    driver.quit()

if __name__ == "__main__":
    user_input = input("Enter the product to search on Amazon: ")
    search_amazon_products(user_input)


# In[4]:


#Q2
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scrape_product_details(product_listing):
    brand_name = product_listing.find("span", class_="a-size-base-plus a-color-base").text.strip()
    product_title = product_listing.find("h2").text.strip()
    price_tag = product_listing.find("span", class_="a-offscreen")
    price = price_tag.text.strip() if price_tag else "-"
    return_exchange = product_listing.find("div", class_="a-row a-size-base a-color-secondary s-align-children-center").text.strip()
    expected_delivery = product_listing.find("div", class_="a-row s-align-children-center").text.strip()
    availability = product_listing.find("div", class_="a-row a-size-base a-color-secondary s-align-children-center").text.strip()
    product_url = product_listing.find("a", class_="a-link-normal").get("href")

    return {
        "Brand Name": brand_name,
        "Name of the Product": product_title,
        "Price": price,
        "Return/Exchange": return_exchange,
        "Expected Delivery": expected_delivery,
        "Availability": availability,
        "Product URL": f"https://www.amazon.in{product_url}"
    }

def search_amazon_products(product_name, num_pages=3):
    driver = webdriver.Chrome()

    driver.get("https://www.amazon.in")

    search_box = driver.find_element("id", "twotabsearchtextbox")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)  

    columns = ["Brand Name", "Name of the Product", "Price", "Return/Exchange", "Expected Delivery", "Availability", "Product URL"]
    df = pd.DataFrame(columns=columns)

    for page in range(1, num_pages + 1):
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "html.parser")

        product_listings = soup.find_all("div", class_="s-result-item")

        for listing in product_listings:
            product_data = scrape_product_details(listing)
            df = df.append(product_data, ignore_index=True)

        next_page_button = driver.find_element_by_link_text(str(page + 1))
        if next_page_button:
            next_page_button.click()
            driver.implicitly_wait(5)

    driver.quit()

    return df

if __name__ == "__main__":
    user_input = input("Enter the product to search on Amazon: ")

    num_pages_to_scrape = 3

    product_df = search_amazon_products(user_input, num_pages_to_scrape)

    product_df.to_csv(f"{user_input}_products.csv", index=False)

    print(f"Product details saved to {user_input}_products.csv")


# In[5]:


#Q3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def download_image(url, folder, filename):
    response = requests.get(url, stream=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    return filepath

def scrape_images(query, num_images=10):
   driver = webdriver.Chrome()

    driver.get("https://www.google.com/imghp")

    search_bar = driver.find_element("name", "q")

    search_bar.send_keys(query)

    search_bar.send_keys(Keys.RETURN)

    time.sleep(2)

    for _ in range(3):  # Adjust the number of scrolls as needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    image_urls = []
    for img in soup.find_all('img', class_='rg_i'):
        data_src = img.get('data-src')
        if data_src:
            image_urls.append(data_src)

    image_urls = image_urls[:num_images]

    folder_name = f"{query}_images"
    os.makedirs(folder_name, exist_ok=True)

    for i, url in enumerate(image_urls, 1):
        filename = f"{query}_{i}.jpg"
        download_image(url, folder_name, filename)
        print(f"Downloaded {filename}")

    driver.quit()

if __name__ == "__main__":
    keywords = ['fruits', 'cars', 'Machine Learning', 'Guitar', 'Cakes']
    for keyword in keywords:
        scrape_images(keyword, num_images=10)


# In[8]:


#Q4
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_flipkart_smartphones(search_query):
    base_url = "https://www.flipkart.com"
    search_url = f"{base_url}/search?q={search_query.replace(' ', '+')}"
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    smartphone_details = []
    results = soup.find_all("div", class_="_1AtVbE")

    for result in results:
        brand_name = result.find("div", class_="_2WkVRV")
        brand_name = brand_name.text.strip() if brand_name else "-"
        
        smartphone_name = result.find("a", class_="IRpwTa")
        smartphone_name = smartphone_name.text.strip() if smartphone_name else "-"
        
        url = result.find("a", class_="IRpwTa")
        url = base_url + url["href"] if url else "-"
        
        price = result.find("div", class_="_30jeq3")
        price = price.text.strip() if price else "-"

        product_response = requests.get(url)
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        details_dict = {"Brand Name": brand_name, "Smartphone Name": smartphone_name, "Price": price, "Product URL": url}

        for row in product_soup.find_all("div", class_="_2RngUh"):
            label = row.find("div", class_="_1k1QCg")
            label = label.text.strip() if label else "-"
            
            value = row.find("div", class_="_3YhLQA")
            value = value.text.strip() if value else "-"
            
            details_dict[label] = value

        smartphone_details.append(details_dict)

    return smartphone_details

#if __name__ == "__main__":
    #user_input = input("Enter the smartphone to search on Flipkart: ")

    #smartphone_details = scrape_flipkart_smartphones(user_input)

    #df = pd.DataFrame(smartphone_details)

    #df = df.replace("", "-")

    #df.to_csv(f"{user_input}_flipkart_results.csv", index=False)

   # print(f"Results saved to {user_input}_flipkart_results.csv")


# In[10]:


#Q5
import requests

def get_coordinates(api_key, city_name):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city_name,
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK" and data.get("results"):
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        print(f"Error: {data['status']} - {data.get('error_message', 'No error message')}")
        return None

if __name__ == "__main__":
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    city_name = input("Enter the city name: ")

    coordinates = get_coordinates(api_key, city_name)

    if coordinates:
        print(f"Coordinates for {city_name}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")


# In[11]:


#Q6
import requests
from bs4 import BeautifulSoup

def scrape_digit_gaming_laptops():
    url = "https://www.digit.in/top-products/best-gaming-laptops-40.html"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

       laptops = soup.find_all("div", class_="TopNumbeHeading sticky-footer")

        for laptop in laptops:
            laptop_name = laptop.find("div", class_="TopNumbeHeading sticky-footer").text.strip()


            print(f"Laptop Name: {laptop_name}")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_digit_gaming_laptops()


# In[12]:


#Q7
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_forbes_billionaires():
    url = "https://www.forbes.com/billionaires/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        billionaires = soup.find_all("div", class_="personName")

        ranks, names, net_worths, ages, citizenships, sources, industries = [], [], [], [], [], [], []

        for idx, billionaire in enumerate(billionaires, 1):
            rank = idx
            name = billionaire.find("div", class_="personName").text.strip()
            net_worth = billionaire.find_next("div", class_="netWorth").text.strip()
            age = billionaire.find_next("div", class_="age").text.strip()
            citizenship = billionaire.find_next("div", class_="countryOfCitizenship").text.strip()
            source = billionaire.find_next("div", class_="source").text.strip()
            industry = billionaire.find_next("div", class_="category").text.strip()

            ranks.append(rank)
            names.append(name)
            net_worths.append(net_worth)
            ages.append(age)
            citizenships.append(citizenship)
            sources.append(source)
            industries.append(industry)

        df = pd.DataFrame({
            "Rank": ranks,
            "Name": names,
            "Net Worth": net_worths,
            "Age": ages,
            "Citizenship": citizenships,
            "Source": sources,
            "Industry": industries
        })

        print(df)

        df.to_csv("forbes_billionaires.csv", index=False)

        print("Data saved to forbes_billionaires.csv")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_forbes_billionaires()


# In[13]:


#Q8
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime

def get_youtube_comments(api_key, video_id, max_results=500):
    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    nextPageToken = None
    total_results = 0

    while total_results < max_results:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(100, max_results - total_results),
                textFormat='plainText',
                pageToken=nextPageToken
            ).execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                upvotes = item['snippet']['topLevelComment']['snippet']['likeCount']
                timestamp = item['snippet']['topLevelComment']['snippet']['publishedAt']

                comments.append({
                    'Comment': comment,
                    'Upvotes': upvotes,
                    'Timestamp': timestamp
                })

            total_results += len(response['items'])
            nextPageToken = response.get('nextPageToken')

            if nextPageToken is None:
                break

        except HttpError as e:
            print(f"An error occurred: {e}")
            break

    return comments

if __name__ == "__main__":
    api_key = 'YOUR_API_KEY'

    video_id = 'YOUR_VIDEO_ID'

    comments_data = get_youtube_comments(api_key, video_id)

    df = pd.DataFrame(comments_data)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df.to_csv("youtube_comments.csv", index=False)

    print("Data saved to youtube_comments.csv")


# In[14]:


#Q9
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_hostels_in_london():
    url = "https://www.hostelworld.com/s?q=London,%20England&country=England&city=London&type=group"
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        hostels = soup.find_all("div", class_="fabresult")

        names, distances, ratings, total_reviews, overall_reviews, privates_prices, dorms_prices, facilities, descriptions = [], [], [], [], [], [], [], [], []

        for hostel in hostels:
            name = hostel.find("h2", class_="title-3").text.strip()
            distance = hostel.find("span", class_="description").text.strip()
            rating = hostel.find("div", class_="rating rating-summary-container big").text.strip()
            reviews = hostel.find("span", class_="reviews").text.strip().replace(" reviews", "")
            overall_review = hostel.find("div", class_="keyword rating-summary").text.strip()
            privates_price = hostel.find("a", class_="prices").find("span", class_="price-col").text.strip()
            dorms_price = hostel.find("a", class_="prices").find("span", class_="price-col").find_next("span").text.strip()
            facility = hostel.find("div", class_="facilities-label").text.strip()
            description = hostel.find("div", class_="description").text.strip()

            names.append(name)
            distances.append(distance)
            ratings.append(rating)
            total_reviews.append(reviews)
            overall_reviews.append(overall_review)
            privates_prices.append(privates_price)
            dorms_prices.append(dorms_price)
            facilities.append(facility)
            descriptions.append(description)

        df = pd.DataFrame({
            "Hostel Name": names,
            "Distance from City Centre": distances,
            "Rating": ratings,
            "Total Reviews": total_reviews,
            "Overall Reviews": overall_reviews,
            "Privates from Price": privates_prices,
            "Dorms from Price": dorms_prices,
            "Facilities": facilities,
            "Property Description": descriptions
        })

        print(df)

        df.to_csv("hostels_in_london.csv", index=False)

        print("Data saved to hostels_in_london.csv")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_hostels_in_london()


# In[ ]:




