from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///circulars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Circular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))
    class_id = db.Column(db.String(20))

#add api
@app.route("/circulars", methods = ["POST"])
def add_circular():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    class_id = data.get("class_id")
    new_circular = Circular(title = title, content = content, class_id = class_id)
    db.session.add(new_circular)
    db.session.commit()
    return jsonify(message = "circular added successfully")


@app.route("/circulars", methods=["GET"])
def get_circulars():
    class_id = request.args.get("class_id")
    if class_id:
        circulars = Circular.query.filter_by(class_id=class_id).all()
    else:
        circulars = Circular.query.all()

    result = []
    for c in circulars:
        result.append({
            "id": c.id,
            "title": c.title,
            "content": c.content,
            "class_id": c.class_id
        })
    return jsonify(result)
if __name__ == "__main__":
    app.run(debug = True)
