from flask import Blueprint, render_template

bp = Blueprint("householder", __name__)

@bp.route("/")
def home():
    return render_template("householder/home.html")

@bp.route("/about")
def about():
    return "Hello, About!"

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/register")
def register():
    return render_template("register.html")