from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import reconcillation
import time
import os

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


with app.app_context():
    db.create_all()
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


@app.route('/')
def home():
    data = db.session.execute(db.select(Book).order_by(Book.name)).scalars()

    return render_template("index.html", books=data.all())


@app.route('/edit/<int:val>', methods=["POST", "GET"])
def edit(val):
    if request.method == "POST":
        print(val)
        book_to_update = db.session.execute(db.select(Book).where(Book.id == val)).scalar()
        book_to_update.rating = float(request.form["name"])
        db.session.commit()
        return redirect(url_for("home"))
    rating_val = db.session.execute(db.select(Book).where(Book.id == val)).scalar()
    return render_template("edit.html", val=rating_val)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        # print(request.form)
        name = request.files["filename"]
        name_of_file = f"{name.filename.split('.')[0]}.txt"
        with open(name_of_file, "w", encoding="utf-8") as f:
            g = bytes(name.stream.read())
            file = reconcillation.convert_to_utf_8(g)
            f.write(file)
        with open(name_of_file, "r", encoding="utf-8") as f:
            work = reconcillation.Reconcilation()
            work.run_file(f)
        # print(name.content_type)
        # file = reconcillation.convert_to_utf_8("upload.log")
        # print("startng")
        # print(file[1:100])



        # with open("download", 'w', encoding="utf-8") as f:
        #     f.write(name)

        data = Book(name=request.form["name"], author=request.form["author"], rating=request.form["rate"])
        db.session.add(data)
        db.session.commit()
        # data = {"name": request.form["name"], "author": request.form["author"], "rate":request.form["rate"]}
        # all_books.append(data)

        # recons = reconcillation.Reconcilation()
        # recons.run_file()
        # print("DONE")
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route('/delete')
def delete():
    id = request.args.get('id')
    book = db.get_or_404(Book, id)
    # book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')

