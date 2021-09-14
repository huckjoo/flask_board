from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb"
mongo = PyMongo(app)


@app.route("/", methods=["GET", "POSt"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        writer = request.form.get("writer")
        board = mongo.db.board
        post = {"title": title, "writer": writer, "description": description}
        board.insert_one(post)
        return render_template("success.html", name=post["writer"])


if __name__ == "__main__":
    app.run(debug=True)
