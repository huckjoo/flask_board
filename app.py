from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, abort
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
        # board라는 Collection에 접근 없으면 생성
        board = mongo.db.board
        post = {"title": title, "writer": writer, "description": description}
        db_post = board.insert_one(post)
        print(db_post)
        return redirect(url_for("board", idx=db_post.inserted_id))


@app.route("/board")
def board():
    if request.args.get("idx"):
        idx = request.args.get("idx")
        board = mongo.db.board
        print("모든 아이템", board.find({}))
        if board.find_one({"_id": ObjectId(idx)}):
            myweb_data = board.find_one({"_id": ObjectId(idx)})
            if myweb_data != "":
                db_data = {
                    "id": myweb_data.get("_id"),
                    "title": myweb_data.get("title"),
                    "description": myweb_data.get("description"),
                    "writer": myweb_data.get("writer"),
                }
                return render_template("board.html", db_data=db_data)
            return abort(404)
        return abort(404)


if __name__ == "__main__":
    app.run(debug=True)
