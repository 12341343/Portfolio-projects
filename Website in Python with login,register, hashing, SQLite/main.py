import flask_login
import sqlalchemy.exc
import werkzeug.security
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
 

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):

    return db.get_or_404(User, user_id)
@app.route('/')
def home():

    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
            new_user = User (
                email = request.form["email"],
                password = werkzeug.security.generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8),
                name = request.form["name"]
            )
            name = request.form['name']
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("secrets", name= name))
        except sqlalchemy.exc.IntegrityError:
            flash("This email already exist, try to log in!")
    return render_template("register.html")





@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":

        mail = request.form['email']
        password = request.form['password']
        result = db.session.execute(db.select(User).where(User.email == mail))

        user = result.scalar()

        try:
            result = db.session.execute(db.select(User).where(User.email == mail))
            user = result.scalar()
            if check_password_hash(user.password, password):
                login_user(user)

                return redirect(url_for('secrets', name =user.name.title()))
        except AttributeError:
            flash('Invalid credentials')

    return render_template('login.html')


@app.route('/secrets')
@login_required
def secrets():
    name = request.args.get('name')
    return render_template("secrets.html", name=name)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download', methods=["GET"])
@login_required
def download():
    if request.method == "GET":
        return send_from_directory('static', path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
