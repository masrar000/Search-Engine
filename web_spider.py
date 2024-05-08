import requests
from bs4 import BeautifulSoup
import sqlite3 #importing database functionality to web crawler

def crawler(start_url, max_pages=100): #wrap the entire crawler process in a function
    conn=sqlite3.connect("crawled_pages.db")
    c=conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            content TEXT,
            cleaned_content TEXT,
            title TEXT,
            outgoing_links TEXT,
            pagerank REAL         
        )
    ''') #table to execute crawled pages
    conn.commit()

    url_frontier=[start_url] #queue respinsible for BFS crawling of website
    visited_pages=set() #keep track of visited pages
    
    #in order to crawl web pages in a BFS manner, we have to use a queue. We keep crawling until queue is empty or we reach a maximum number of pages and for this, we need a while loop
    while url_frontier and len(visited_pages)<max_pages:
        url=url_frontier.pop(0) #contain first url of url frontier
        #skip the page if we already visited
        if url in visited_pages:
            continue
        print(f"Crawling {url}")
        
        response=requests.get(url)
        # print(response.content) if you want to check the content of the HTML page

        #skip the page if it has error
        if response.status_code!=200:
            continue

        soup=BeautifulSoup(response.content, "html.parser")#using Beautiful Soup to parse content of the HTML page
        
        #now extract the title of web pages
        if soup.find("title"):
            title=soup.find("title").string
        
        outgoing_links=[] #compute the links of all
        #loop over all the links extracted from soup variable
        for link in soup.find_all("a"): #this will find all anchor tags
             href=link.get("href")
             if href: #if href exists
                 outgoing_links.append(href)

        #? is just for filling the 5 positions of url, content, cleaned_content,title,outgoing_links 
        c.execute("INSERT OR REPLACE INTO pages(url,content, cleaned_content, title,outgoing_links) VALUES (?,?,?,?,?)",
                  (url, str(soup),soup.get_text(), title,",".join(outgoing_links))) #get the text out of the soup and remove all the tags
        
        #, joins all the elements of the outgoing_links list
        conn.commit() #save the content of the database

        links=soup.find_all("a")
        #print(links) #prints all anchor tags (a tags) in the soup
        #print href attributes of a tags (this is the URL)
        
        for link in links:
            href = link.get("href")
            #print(href) #when you print this, you also get relative useless links that are not the URL
        #print URLs only
        #'''
            if href and "http" in href and href not in visited_pages:  # Ensure href is not None and contains 'http'
                url_frontier.append(href)   #possible if href not None type and http in href and href not in visited set
        #mark current page as visited at the end
        visited_pages.add(url)
        #'''

    conn.close()
    #print a message that crawling is complete
    print("Crawling complete")


#calling the function
seed_urls=["https://www.bbc.co.uk/news/topics/cp29jzed52et",
           "https://www.cnn.com"]
for url in seed_urls:
    crawler(url,50) #crawling 50 links from bb.co/.. and cnn.com each

#the crawled pages will be saved on crawled_pages.db

#now calculating page rank of the pages that have been crawled in a new file called pagerank.py