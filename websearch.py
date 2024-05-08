from flask import Flask, request, render_template
import sqlite3

app=Flask(__name__, template_folder="./static") #Defining a flask app

#Creating a static folder in 5 Web Search Engine using Database

#Creating default route
@app.route("/")
def home():
    return render_template("websearch.html")

@app.route("/websearch", methods=["GET","POST"])
def search():
    #get query from request
    query=request.form["query"]

    if query=="":
        render_template("websearch.html")
    
    #Connect to the sqlite database
    conn=sqlite3.connect("crawled_pages.db")
    cursor=conn.cursor()

    #Search for websites that match query in their cleaned_content
    cursor.execute("SELECT url, title FROM pages WHERE cleaned_content LIKE ? ORDER BY pagerank DESC", ("%"+ query +"%",))
    urls=cursor.fetchall()
    conn.close() #close the connection

    #Render the URLS that match the query as HTML template
    return render_template("results.html",urls=urls, query=query)


#this makes sure that we just run websearch.py
if __name__=="__main__":
    app.run(debug=True)