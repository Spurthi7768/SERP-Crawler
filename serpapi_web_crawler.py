from serpapi import GoogleSearch
from pytube import YouTube
from pytube import Channel
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(".env")
API_KEY=os.getenv("API")

def generate_modified_data():
    
    #Open the file and load the data
    file = open("output/data_raw.json")
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

    with open('output/data_modified_serpapi.json', 'w') as f:
        json.dump(list_modified_links, f)

def generate_raw_data(results):
  list_links=[]

  #iterate through the generated dictionary

  for result in results["organic_results"]:       
    dictionary={"Title": f"{result['title']}", "Link": f"{result['link']}"}
    list_links.append(dictionary)

  if(os.path.exists(os.path.join(os.getcwd(), 'output'))):
     with open('output/data_raw.json', 'w') as f:
      json.dump(list_links, f)
  else:
    os.mkdir(os.path.join(os.getcwd(), 'output'))
    with open('output/data_raw.json', 'w') as f:
      json.dump(list_links, f)


#Parameters to be passed to the SerpAPI
params = {
  "engine": "google",
  "num": "10000", #number of results
  "q": "site:youtube.com openinapp.co", #query to be sent
  "google_domain": "google.com",
  "gl": "us",
  "hl": "en",
  "location": "Austin, Texas, United States",
  "api_key": f"{API_KEY}"
}


if __name__=='__main__':
  search = GoogleSearch(params)
  results = search.get_dict()
  generate_raw_data(results)
  generate_modified_data()



