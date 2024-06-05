from flask import Flask, request, render_template
import mysql.connector

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
    print("*"*10)
    print("Query:", query)
    print("*"*10)

    if query=="":
        render_template("websearch.html")
    
    # MySQL connection parameters
    mySQLparams = {
        'host': 'localhost',
        'user': 'root',
        'database': 'MY_CUSTOM_BOT',
        'password': '1234'
    }
    
    connection = mysql.connector.connect(**mySQLparams)
    cursor = connection.cursor()
    
    cols = ["childhood_count", "cancer_count", "early_count", "diagnosis_count", "methods_count"]
    q_string = ""
    
    for term in query.split(" "):
        c = term + "_count"
        if q_string == "":
            q_string = q_string + c
        else:
            q_string = q_string + " + " + c
    
    sql_query = '''SELECT url, title from 
                (SELECT sr.url, sr.title, sum(''' + q_string + ''') 
                 as total_sum FROM search_results_v2 sr 
                 inner join URL_frequency uf 
                 on sr.url_id = uf.url_id 
                group by sr.url_id
                order by total_sum desc) a'''
    
    #Search for websites that match query in their cleaned_content
    cursor.execute(sql_query)
                   
    urls=cursor.fetchall()
    connection.close() #close the connection
    print("urls",urls)
    #Render the URLS that match the query as HTML template
    return render_template("results.html",urls=urls, query=query)


#this makes sure that we just run websearch.py
if __name__=="__main__":
    app.run(debug=True)