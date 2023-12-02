#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Q1
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_header_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    header_tags = [f'h{i}' for i in range(1, 7)]
    headers = soup.find_all(header_tags)
    return [header.text.strip() for header in headers]

# URL of the Wikipedia homepage
wikipedia_url = 'https://en.wikipedia.org/wiki/Main_Page'

header_tags = get_header_tags(wikipedia_url)

df = pd.DataFrame({'Header Tags': header_tags})

df


# In[24]:


#Q2
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get former presidents from the given URL
def get_former_presidents(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    presidents_table = soup.find('table', {'class': 'table-responsive'})
    
    presidents_data = []
    for row in presidents_table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        name = columns[0].text.strip()
        term_of_office = columns[1].text.strip()
        presidents_data.append({'Name': name, 'Term of Office': term_of_office})
    
    return presidents_data

# URL of the page with the list of former presidents
presidents_url = 'https://presidentofindia.nic.in/former-presidents.htm'

# Get former presidents
former_presidents = get_former_presidents(presidents_url)

# Create a DataFrame
df_presidents = pd.DataFrame(former_presidents)

# Display DataFrame
df_presidents


# In[8]:


#Q6 
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get details of most downloaded articles
def get_most_downloaded_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    for article in soup.find_all('div', class_='pod-listing-header'):
        title = article.find('a', class_='pod-listing-title').text.strip()
        authors = article.find('div', class_='pod-listing-authors').text.strip()
        published_date = article.find('div', class_='pod-listing-date').text.strip()
        paper_url = article.find('a', class_='pod-listing-title')['href']
        
        articles.append({
            'Paper Title': title,
            'Authors': authors,
            'Published Date': published_date,
            'Paper URL': paper_url
        })
    
    return articles

# URL of the most downloaded articles page
url = 'https://www.journals.elsevier.com/artificial-intelligence/most-downloaded-articles'

# Get most downloaded articles
most_downloaded_articles = get_most_downloaded_articles(url)

# Create a DataFrame
df_articles = pd.DataFrame(most_downloaded_articles)

# Display DataFrame
df_articles


# In[9]:


#Q5 
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get news details
def get_cnbc_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_list = []
    for news in soup.find_all('div', class_='Card-titleContainer'):
        headline = news.find('a', class_='Card-titleLink').text.strip()
        time = news.find('span', class_='Card-time').text.strip()
        news_link = news.find('a', class_='Card-titleLink')['href']
        
        news_list.append({
            'Headline': headline,
            'Time': time,
            'News Link': news_link
        })
    
    return news_list

# URL of the CNBC news page
url = 'https://www.cnbc.com/world/?region=world'

# Get CNBC news details
cnbc_news = get_cnbc_news(url)

# Create a DataFrame
df_news = pd.DataFrame(cnbc_news)

# Display DataFrame
df_news


# In[10]:


#Q4
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get top 10 ODI teams, players, and all-rounders
def get_icc_cricket_rankings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get top 10 ODI teams
    teams_data = []
    teams_table = soup.find('table', class_='table rankings-table')
    for row in teams_table.find('tbody').find_all('tr')[:10]:
        columns = row.find_all('td')
        team_name = columns[1].text.strip()
        matches = columns[2].text.strip()
        points = columns[3].text.strip()
        rating = columns[4].text.strip()
        teams_data.append({
            'Team': team_name,
            'Matches': matches,
            'Points': points,
            'Rating': rating
        })
    
    # Get top 10 women's ODI batting players
    batting_data = []
    batting_table = soup.find('table', class_='table rankings-table')
    for row in batting_table.find_all('tr', class_='rankings-block__banner')[:1] +                batting_table.find_all('tr', class_='table-body')[:9]:
        columns = row.find_all('td')
        player_name = columns[1].text.strip()
        team_name = columns[2].text.strip()
        rating = columns[4].text.strip()
        batting_data.append({
            'Player': player_name,
            'Team': team_name,
            'Rating': rating
        })
    
    # Get top 10 women's ODI all-rounders
    all_rounders_data = []
    all_rounders_table = soup.find_all('table', class_='table rankings-table')[1]
    for row in all_rounders_table.find_all('tr', class_='rankings-block__banner')[:1] +                all_rounders_table.find_all('tr', class_='table-body')[:9]:
        columns = row.find_all('td')
        player_name = columns[1].text.strip()
        team_name = columns[2].text.strip()
        rating = columns[4].text.strip()
        all_rounders_data.append({
            'Player': player_name,
            'Team': team_name,
            'Rating': rating
        })
    
    return teams_data, batting_data, all_rounders_data

# URL for women's ODI rankings on ICC website
url = 'https://www.icc-cricket.com/rankings/womens/team-rankings/odi'

# Get ICC cricket rankings
teams_data, batting_data, all_rounders_data = get_icc_cricket_rankings(url)

# Create DataFrames
df_teams = pd.DataFrame(teams_data)
df_batting = pd.DataFrame(batting_data)
df_all_rounders = pd.DataFrame(all_rounders_data)

# Display DataFrames
print("Top 10 ODI Teams:")
print(df_teams)

print("\nTop 10 Women's ODI Batting Players:")
print(df_batting)

print("\nTop 10 Women's ODI All-rounders:")
print(df_all_rounders)


# In[11]:


#Q3
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get top 10 ODI teams, batsmen, and bowlers
def get_icc_cricket_rankings(url_teams, url_batsmen, url_bowlers):
    # Function to get data for a ranking table
    def get_ranking_data(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = []
        table = soup.find('table', class_='table rankings-table')
        for row in table.find('tbody').find_all('tr')[:10]:
            columns = row.find_all('td')
            name = columns[1].text.strip()
            team = columns[2].text.strip()
            rating = columns[3].text.strip()
            data.append({
                'Name': name,
                'Team': team,
                'Rating': rating
            })
        return data
    
    # Get top 10 ODI teams
    teams_data = get_ranking_data(url_teams)
    
    # Get top 10 ODI batsmen
    batsmen_data = get_ranking_data(url_batsmen)
    
    # Get top 10 ODI bowlers
    bowlers_data = get_ranking_data(url_bowlers)
    
    return teams_data, batsmen_data, bowlers_data

# URLs for men's ODI rankings on ICC website
url_teams = 'https://www.icc-cricket.com/rankings/mens/team-rankings/odi'
url_batsmen = 'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting'
url_bowlers = 'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling'

# Get ICC cricket rankings
teams_data, batsmen_data, bowlers_data = get_icc_cricket_rankings(url_teams, url_batsmen, url_bowlers)

# Create DataFrames
df_teams = pd.DataFrame(teams_data)
df_batsmen = pd.DataFrame(batsmen_data)
df_bowlers = pd.DataFrame(bowlers_data)

# Display DataFrames
print("Top 10 ODI Teams in Men's Cricket:")
print(df_teams)

print("\nTop 10 ODI Batsmen in Men's Cricket:")
print(df_batsmen)

print("\nTop 10 ODI Bowlers in Men's Cricket:")
print(df_bowlers)


# In[25]:


import requests
from bs4 import BeautifulSoup
def timesofindia():
    url = "https://timesofindia.indiatimes.com/home/headlines"
    page_request = requests.get(url)
    data = page_request.content
    soup = BeautifulSoup(data,"html.parser")

    counter = 0
    for divtag in soup.find_all('div', {'class': 'headlines-list'}):
        for ultag in divtag.find_all('ul', {'class': 'clearfix'}):
            if (counter <= 10):
                for litag in ultag.find_all('li'):
                    counter = counter + 1
                    print(str(counter) + " - https://timesofindia.indiatimes.com" + litag.find('a')['href'])
                    #print(str(counter) + "." + litag.text + " - https://timesofindia.indiatimes.com" + litag.find('a')['href'])

if __name__ == "__main__":
    timesofindia()


# In[17]:


#Q7
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get restaurant details
def get_dineout_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    restaurants = []
    
    for card in soup.find_all('div', class_='restnt-card'):
        name = card.find('h3', class_='restnt-name').text.strip()
        cuisine = card.find('p', class_='double-line-ellipsis').text.strip()
        location = card.find('p', class_='restnt-loc').text.strip()
        ratings = card.find('div', class_='restnt-rating').text.strip()
        img_url = card.find('img', class_='img-responsive')['src']
        
        restaurants.append({
            'Restaurant Name': name,
            'Cuisine': cuisine,
            'Location': location,
            'Ratings': ratings,
            'Image URL': img_url
        })
    
    return restaurants

# URL of the dineout.co.in page with restaurant details
url = 'https://www.dineout.co.in/delhi-restaurants'

# Get restaurant details
dineout_data = get_dineout_data(url)

# Create a DataFrame
df_dineout = pd.DataFrame(dineout_data)

# Display DataFrame
df_dineout


# In[19]:


pip install beautifulsoup4


# In[21]:


pip install pandas


# In[22]:


pip install requests


# In[26]:


#Q2
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the website
url = "https://presidentofindia.nic.in/former-presidents.htm"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the data
table = soup.find("table")

# Create empty lists to store the data
names = []
terms = []

# Iterate over each row in the table
for row in table.find_all("tr")[1:]:
  # Extract the name and term of office from the columns
  columns = row.find_all("td")
  name = columns[0].text.strip()
  term = columns[1].text.strip()
  
  # Append the data to the respective lists
  names.append(name)
  terms.append(term)

# Create a data frame using the lists
data = {"Name": names, "Term of Office": terms}
df = pd.DataFrame(data)

# Display the data frame
print(df)


# In[ ]:




