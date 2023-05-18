import os

from flask import Flask
from flask import render_template

from database import db, Book, Genre, Author

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # creating and adding genres
    comedy = Genre(name='Комедия')
    db.session.add(comedy)
    story = Genre(name='Повесть')
    db.session.add(story)

    # creating and adding authors
    fonvizin = Author(name='Д.И.Фонвизин')
    db.session.add(fonvizin)
    griboedov = Author(name='А.С.Грибоедов')
    db.session.add(griboedov)
    pushkin = Author(name='А.С.Пушкин')
    db.session.add(pushkin)

    # creating and adding books
    nedorosl = Book(name='Недоросль', genre=comedy, author=fonvizin)
    db.session.add(nedorosl)
    woe_from_wit = Book(name='Горе от ума', genre=comedy, author=griboedov)
    db.session.add(woe_from_wit)
    capitans_daughter = Book(name='Капитанская дочка', genre=story, author=pushkin)
    db.session.add(capitans_daughter)

    db.session.commit()


@app.route("/")
def all_books():
    books = Book.query.all()
    return render_template("books.html", books=books)


@app.route("/genre/<int:genre_id>")
def books_by_genres(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        "books_by_genres.html",
        genre_name=genre.name,
        books=genre.books,
    )


@app.route("/author/<int:author_id>")
def books_by_author(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template(
        "books_by_author.html",
        author_name=author.name,
        books=author.books
    )



if __name__ == '__main__':
    app.run()