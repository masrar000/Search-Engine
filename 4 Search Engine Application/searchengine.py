from flask import Flask,render_template,request
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

app = Flask(__name__, template_folder="./static/")

# adding route from websearch.html
@app.route("/")
def websearch():
    return render_template("websearch.html")



@app.route("/a")
def a():
    return render_template("A.html") #to render it, we have to register template directory and this register is to be done in app variable


@app.route("/b")
def b():
    return render_template("B.html")

@app.route("/c")
def c():
    return render_template("C.html")

@app.route("/d")
def d():
    return render_template("D.html")

@app.route("/e")
def e():
    return render_template("E.html")

@app.route("/websearch",methods=["GET","POST"])
def web_search(): #websearch is already defined above so make it web_search for difference
#This prevents flask from throwing an error for same functioning
    if request.method=="POST":
        query=request.form["query"]
        if query=="":
            return render_template("websearch.html")
        websites=["http://localhost:5000/a",
            "http://localhost:5000/b",
            "http://localhost:5000/c",
            "http://localhost:5000/d",
            "http://localhost:5000/e"]

        
        tokenized_text=load_tokenized_text("tokenized_text_pickle.pkl") #loading the tokenized text
        #calculating TF-IDF of tokenized text
        #TF-IDF means term frequency inverse document frequency
        tfidf=TfidfVectorizer()
        tfidf_vectors=tfidf.fit_transform([" ".join(tokens) for tokens in tokenized_text]) #the tf-idf term represents docuemnts as rows and vocabulary terms as columns
        
        #now searching using cosine similarity
        query_vector=tfidf.transform([query])
        similarities=cosine_similarity(query_vector,tfidf_vectors)
        #print(similarities) #running this will generate a 1 by 5 matrix with each value showing similairty score of each web page with respect to the query

        if all_zeros(similarities[0]):
            return render_template("notfound.html")
        
        #now calculating pagerank but
        #first we create a directed graph and find similarity score
        G=nx.DiGraph()
        #now looping over websites
        for i, link in enumerate(websites):
            G.add_node(link) #link is the link to the website
            for j,sim in enumerate(similarities[0]):
                if sim >0 and i !=j: #if there is a similarity between query and TF-IDF transform vector
                    G.add_edge(link,websites[j], weight=sim)

        pagerank= nx.pagerank(G) #now we can calculate pagerank
        ranked_results=sorted(pagerank.items(), key=lambda x:x[1], reverse=True) #sort the files by pagerank
        top_results=[x[0] for x in ranked_results if x[1] >=0.14] #return top results (Assuming 0.14 is the optimum value, it can be experimented around)
     #0.14 generally worls for 5 web pages
        print(top_results)
        return  render_template("results.html", data=[top_results, query]) #displays query in results.html

#now we just have to render the results in a systematic format in results.html  
    

def load_tokenized_text(filename):
    tokenized_text=pickle.load(open(filename,"rb")) #rb means read binary
    return tokenized_text

def all_zeros(l): #it will take list l as parameters
    for i in l:
        if i !=0:
            return False
    return True


#wheneerv you write a command in flask, you have to restart flask again.
#automating this process to update the page automatically
if __name__=="__main__":
    app.run(debug=True)
#now you dont have to type flask --app searchengine run, 
#just type python searchengine.py