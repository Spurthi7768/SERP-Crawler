from bs4 import BeautifulSoup
import requests, lxml
import json
from tqdm import tqdm
import random
from pytube import YouTube
import os

#Parameters for the request
params = {
    "q": "site:youtube.com openinapp.co",
    "hl": "en",         # language
    "gl": "us",         # country of the search, US -> USA
    "filter": 0         # show all pages by default up to 10
}

#List of user agents for the request
user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
]

list_links=[]  #List of dictionaries created


def generate_modified_data():
    
    #Open the file and load the data
    file = open("output/data_raw_manual.json")
    data = json.load(file)

    #Create a list of dictionaries
    list_modified_links=[]

    #Iterate through the loaded data
    for item in data:
      
      try:
        video_link=YouTube(str(item['Link']))
        Channel_URL=video_link.channel_url
        dict={"Title": f"{item['Title']}", "Video Link": f"{item['Link']}","Channel Link":f"{Channel_URL}"} #Create the dictionary structure
        list_modified_links.append(dict)
      except:    
        dict={"Title": f"{item['Title']}", "Video Link": f"{item['Link']}","Channel Link":f"{item['Link']}"}
        list_modified_links.append(dict)
    
    #Write the modified data into a json file

    with open('output/data_modified_manual.json', 'w') as f:
        json.dump(list_modified_links, f)

def generate_raw_data():
  
  #Create a output directory to store jsons if it does not exist
  if(os.path.exists(os.path.join(os.getcwd(), 'output'))):
     with open('output/data_raw_manual.json', 'w') as f:
      json.dump(list_links, f)
  else:
    os.mkdir(os.path.join(os.getcwd(), 'output'))
    with open('output/data_raw_manual.json', 'w') as f:
      json.dump(list_links, f)

def bs4_scrape(num):
    page=1 #Number of pages 
    start=0 
    query="site:youtube.com+openinapp.co" #query to be searched
    pbar = tqdm(total=10000) #Progress bar
    user_agent = random.choice(user_agents)
    headers = {
                'User-Agent': user_agent
    }  
    while page<=num: #pages should be around 1000 for 10000 results since 10 results per page
        #request to be sent
        html = requests.get("https://www.google.com/search?q={}&start={}".format(query,start), headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, 'lxml') 

        for result in soup.select(".yuRUbf"):    #Channel links in the result
           
            dict={'Title': f'{result.select_one("h3").text}', 'Link':f'{result.select_one("a")["href"]}'}                     
            list_links.append(dict)
        
        
        
        for result in soup.select(".DhN8Cf"): #Video links in the result
            dict={'Title': f'{result.select_one("h3").text}', 'Link':f'{result.select_one("a")["href"]}'}      
            list_links.append(dict)
        
        start += 10 
        page+=1
        pbar.update(start-pbar.n)    #update the progress bar
    
    pbar.close()

    

if __name__=='__main__':
    bs4_scrape(1001)
    generate_raw_data()
    generate_modified_data()




