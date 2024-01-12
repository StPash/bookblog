from flask import Flask, render_template, url_for, request, flash, redirect
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker
from create_test_bd_books import Base, Book, Genre, BookGenre, Author, User
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dn1y6hjm8u3wr44yg6hn7i'
engine = create_engine('sqlite:///db_books_log.db')
session = sessionmaker(bind=engine)

# Жанры из БД в словарь
genredict = {}
with session() as db:
    for row in db.query(Genre).all():
        genredict[row.id_genre] = row.name


# Главная
@app.route('/')
def index():
    with session() as db:
        result = db.query(Book).order_by(func.random()).limit(3).all()

        return render_template('index.html',
                               result=result,
                               genredict=genredict)


# Список авторов
@app.route('/authors')
def authors():
    with session() as db:
        return render_template('authors.html',
                               db=db,
                               Author=Author)


# Список книг автора
@app.route('/authors/<author_id>/')
def author_books(author_id):
    with session() as db:
        booklist = db.query(Book).filter(Book.author_id == author_id).all()
        return render_template('booklist.html',
                               booklist=booklist,
                               genredict=genredict)


# Выбор жанров
@app.route('/genres')
def genres():
    return render_template('genres.html', genredict=genredict)


@app.route('/t')
def test():
    with session() as db:
        return render_template('test.html', Book=Book, db=db)


# Список книг по жанрам
@app.route('/genrebooks', methods=['POST'])
def genrebooks():
    genre_list = request.form.keys()
    with session() as db:
        id_book_list = set(db.query(BookGenre.book_id).filter(BookGenre.genre_id.in_(genre_list)).all())
        booklist = db.query(Book).filter(Book.id_book.in_(map(lambda x: x[0], id_book_list))).all()
        return render_template('genrebooks.html', booklist=booklist, genredict=genredict)


# Авторизация
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if len(request.form['name']) < 3:
            flash('Ошибка регистрации. Имя пользователя должно содержать не менее 3 символов.',
                  category='error')
        elif '@' not in request.form['email'] and '.' not in request.form['email']:
            flash('Ошибка регистрации. Неверно введён адрес электронной почты.',
                  category='error')
        elif len(request.form['psswrd']) < 6:
            flash('Ошибка регистрации. Пароль должен содержать не менее 6 символов.',
                  category='error')
        elif request.form['psswrd'] != request.form['psswrd2']:
            flash('Ошибка регистрации. Пароли не совпадают.',
                  category='error')
        else:
            new_user = User(name=request.form['name'],
                            email=request.form['email'],
                            password_hash=generate_password_hash(request.form['psswrd'])
                            )
            with session() as db:
                db.add(new_user)
                db.commit()
            flash('Вы успешно зарегистрировались',
                  category='success')
            return redirect('/login')
    return render_template('register.html')




if __name__ == '__main__':
    app.run(debug=True)
