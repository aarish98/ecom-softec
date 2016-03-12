import os
from datetime import datetime
from flask import Flask, render_template, request, make_response, Response, url_for, flash, session
from flask.ext.login import LoginManager
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.utils import redirect
from faker import Factory
from models import db, Users, Categories, Products

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.secret_key = 'some_secret'

db.app = app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

faker = Factory.create()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if current_user.is_authenticated:
        return redirect("/")
    email = request.form["email"]
    password = request.form["password"]

    registered_email = Users.query.filter_by(email=email).first()
    if registered_email is None:
        return redirect(url_for('.login'))
    if not registered_email.check_password(password):
        return redirect(url_for('.login'))

    login_user(registered_email)
    return redirect(request.args.get('next') or url_for('.index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    check_password = request.form["checkpassword"]

    if Users.query.filter_by(email=email).first():
        flash("User Exists with that Email")
        return redirect(url_for('.register'))

    if not email.strip() or not password.strip() or not name.strip() or check_password != password:
        flash("Error Occured")

    user = Users(name, password, email)
    db.session.add(user)
    db.session.commit()

    flash("Successfully registered")

    return redirect(url_for('.login'))


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/create/product", methods=["GET", "POST"])
@login_required
def create_product():
    if request.method == "GET":
        return render_template("/create-product.html")

    product_name = request.form["product-name"]
    product_color = request.form["product-color"]
    product_description = request.form["product-description"]
    product_size = request.form["product-size"]
    original_quantity = request.form["original-quantity"]

    product = Products(product_name, product_color, product_size, original_quantity, product_description)
    current_user.products_created.append(product)
    Categories.query.filter_by(id=1).first().products.append(product)

    db.session.add(product)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/categories")
def categories():
    all_categories = Categories.query.all()
    return render_template("categories.html", all_categories=all_categories)


@app.route("/category/<id>")
def category(id):
    try:
        id = int(id)
    except:
        flash("No Such Category Found")
        return redirect(url_for("index"))

    if not Categories.query.get(id):
        flash("No Such Category Found")
        return redirect(url_for("index"))

    category = Categories.query.get(id)
    return render_template("category.html", category=category)


@app.route("/product/<id>")
def product(id):
    try:
        id = int(id)
    except:
        flash("No Such Product Found")
        return redirect(url_for("index"))

    if not Products.query.get(id):
        flash("No Such Product Found")
        return redirect(url_for("index"))

    product = Products.query.get(id)
    return render_template("product.html", product=product)


if __name__ == "__main__":
    if not os.path.exists('main.db'):
        db.create_all()
        db.session.add(Users("Hassaan Ali Wattoo", "test", "test"))
        for i in range(0, 20):
            db.session.add(Categories(faker.company()))
        db.session.commit()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
