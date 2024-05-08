import sqlite3
import networkx as nx

#Connecting to the SQLITE database
conn=sqlite3.connect("crawled_pages.db") #establish connections with 
cursor=conn.cursor()

#Retrieve URLs of all websites from the database
cursor.execute("SELECT url FROM pages")
urls=[row[0] for row in cursor.fetchall()] #Assign URLs from row to URLs variable

#Creating an empty directed graph using netowrkx for pagerank
graph=nx.DiGraph()

#Add the nodes to the graph
for url in urls:
    graph.add_node(url)

#Retrieve the outgoing links of each website from the database 
#and add the edges to the graph
for url in urls:
    cursor.execute("SELECT outgoing_links FROM pages WHERE url=?", (url, ))
    outgoing_links=cursor.fetchone()[0].split(",")
    for link in outgoing_links:
        if link.startswith("http"):
            graph.add_edge(url,link)

pagerank=nx.pagerank(graph) #Calculate pagerank of the graph

#Store the pagerank scores in the database
for url in urls:
    cursor.execute("UPDATE pages SET pagerank=? WHERE url =?",
                   (pagerank[url],url))


conn.commit() #Commit the changes to the database
conn.close()#close the database connection


    







 




