from flask import Flask,render_template

app = Flask(__name__, template_folder="./static/")


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

#wheneerv you write a command in flask, you have to restart flask again.
#automating this process to update the page automatically
if __name__=="__main__":
    app.run(debug=True)
#now you dont have to type flask --app searchengine run, 
#just type python searchengine.py