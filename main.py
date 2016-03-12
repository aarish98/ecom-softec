import os
from datetime import datetime
from flask import Flask, render_template, request, make_response, Response, url_for, flash
from flask.ext.login import LoginManager
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.utils import redirect

from models import db,User

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.secret_key = 'some_secret'

db.app = app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=["GET","POST"])
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if current_user.is_authenticated:
        return redirect("/")
    email = request.form["email"]
    password = request.form["password"]

    registered_email = User.query.filter_by(email=email).first()
    if registered_email is None:
        return redirect(url_for('.login'))
    if not registered_email.check_password(password):
        return redirect(url_for('.login'))

    login_user(registered_email)
    return redirect(request.args.get('next') or url_for('.index'))


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    check_password = request.form["checkpassword"]

    if User.query.filter_by(email=email).first():
        flash("User Exists with that Email")
        return redirect(url_for('.register'))

    if not email.strip() or not password.strip() or not name.strip() or check_password != password:
        flash("Error Occured")

    user = User(name, password, email)
    db.session.add(user)
    db.session.commit()

    flash("Successfully registered")

    return redirect(url_for('.login'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    if not os.path.exists('main.db'):
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
