from flask import Flask, render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap
from flask_login import UserMixin
from moviedata import search_movie
from form import RegisterForm, LoginForm, SearchForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sfsKR6b'
db = SQLAlchemy(app)
Bootstrap(app)


login_manager = LoginManager()
login_manager.__init__(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    movies = relationship("MoviesData", back_populates="movie")


class MoviesData(db.Model):
    __tablename__ = "Movies Data"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    movie = relationship("User", back_populates="movies")
    title = db.Column(db.String)
    year = db.Column(db.String)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    img_url = db.Column(db.String(200))


db.create_all()


@app.route("/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user_check = db.session.query(User).filter_by(email=form.email.data).first()
        if new_user_check and new_user_check.email == form.email.data:
            flash('Email already Registered , Login Instead')
            return redirect(url_for('login'))
        else:
            hash_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = User(name=form.name.data, email=form.email.data, password=hash_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('homepage'))
            else:
                flash('Incorrect Password')
                return redirect('login')
        else:
            flash("Email Doesn't exist , SignUp Instead")
            return redirect(url_for('register'))
    return render_template("login.html", form=form)


@app.route('/add')
@login_required
def add_to_db():
    title = request.args.get('title')
    description = request.args.get('description')
    year = request.args.get('release_date')
    rating = request.args.get('rating')
    url = request.args.get('img_url')
    if len(description) < 600:
        for _ in range(1000 - len(description)):
            description += " "
    print(len(description))
    data = MoviesData(user_id=current_user.id, title=title, year=year, description=description, rating=rating, img_url=url)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('homepage'))


@app.route('/logout')
def logout_use():
    logout_user()
    return redirect(url_for('register'))


@app.route('/delete')
@login_required
def delete():
    id = request.args.get('movie_id')
    movie_to_delete = MoviesData.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('homepage', user_id=current_user.id))


@app.route('/readme')
def readme():
    id = request.args.get('user_id')
    return render_template('readme.html', user_id=id)


@app.route('/homepage')
def homepage():
    movies = db.session.query(MoviesData).filter_by(user_id=current_user.id)
    ordered_movies = db.session.query(MoviesData).filter_by(user_id=current_user.id).order_by(MoviesData.rating.desc()).all()[:3]
    print([n.title for n in ordered_movies])
    print(current_user.name)
    return render_template('index2.html', movies=movies, top_movies=ordered_movies, username=current_user.name)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        movie = form.movie_name.data
        try:
            data = search_movie(movie)
            print(data)
            return render_template('search2.html', form=form, all_data=data, username=current_user.name)
        except IndexError:
            flash('Invalid Movie Detials')
            flash('Tip1 : Check movie name Spelling')
            flash('Tip2 : Space for two words is mandatory')
            flash('Tip3 : If both tip1 and tip2 doesnt work check spelling of the movie from the Internet ')
            return redirect('search')
    return render_template('search2.html', form=form, username=current_user.name)


if __name__ == '__main__':
    app.run(debug=True)