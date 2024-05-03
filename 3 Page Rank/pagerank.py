import requests
from bs4 import BeautifulSoup
import networkx as nx #to rank pages

#list iwth urls to crawl
urls=["http://127.0.0.1:5000/a",
      "http://127.0.0.1:5000/b",
      "http://127.0.0.1:5000/c",
      "http://127.0.0.1:5000/d",
      "http://127.0.0.1:5000/e"
]

outgoing_links={}
for url in urls:
    reponse=requests.get(url) #get the response
    soup=BeautifulSoup(reponse.text,"html.parser") #parse the response
    links=[link.get("href") for link in soup.find_all("a") if link.get("href")] #collect all links in soup by finding all links with a and href as we had previously seen
    outgoing_links[url]=links

#print(outgoing_links) #will show the link pointing to list of links in a dictionary

G=nx.DiGraph()

for node,links in outgoing_links.items():
    G.add_node(node) #adding nodes
    for link in links: #adding edges so looping each list in print(outgoing_links)
        G.add_edge(node,link) #adds edge from one node to another using link

pagerank=nx.pagerank(G,weight="weight")
ranked_results=sorted(pagerank.items(),key=lambda x:x[1], reverse=True) #display the results in sorted manner and the sorting is going to be done according to the pagerank of the page
#top_results=ranked_results[:4] #print the top 4 results
#print(top_results)
print(ranked_results) #to display all results

