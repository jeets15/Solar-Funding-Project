from collections import namedtuple
import functools
from email_validator import EmailNotValidError, validate_email
from flask import Blueprint, abort, g, render_template, flash, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from solar_offset.db import get_db
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
from uuid import uuid4
import os

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
bp = Blueprint("auth", __name__, url_prefix="/auth")

def email_is_valid(email):
    ReturnObj = namedtuple("EmailInfo", ['is_valid', 'email', 'error'])
    # Validate email
    try:
        emailinfo = validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        return ReturnObj(False, email, e)
    else:
        return ReturnObj(True, emailinfo.normalized, None)

# This function is called before every request is processed by a view
# Assigns the record of the currently logged in user to g.user
# Otherwise g.user is None
@bp.before_app_request
def load_logged_in_user():
    # Ignore static requests
    if request.endpoint == 'static':
        return None

    user_id = session.get('user_id', None)
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        if user is None:
            g.user = None
        else:
            user = dict(user)
            if user['display_name']:
                user['name'] = user['display_name']
            else:
                user['name'] = user['email_username']
            g.user = user

    # Handle when a user is suspended
    # All requests are automatically redirected to the 'suspended' page
    if g.user \
        and (g.user['status_suspend'] is not None) \
        and request.endpoint != 'auth.logout' \
        and request.endpoint != 'auth.account_suspended':
        return redirect(url_for('auth.account_suspended'))


# Decorator that can be used to force user to be logged in for a page
# Optionally, specify which user types are allowed and which not
def login_required(allowed_user_types=None):
    set_allowed_user_types = None
    if allowed_user_types:
        set_allowed_user_types = set(allowed_user_types)

    def _wrapper(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                flash("You must log in to view this page", "danger")
                return redirect(url_for('auth.login'))
            elif set_allowed_user_types:
                set_user_types = set(g.user['user_type'].replace("_", ""))
                if not set_user_types.intersection(set_allowed_user_types):
                    flash("You don't have permission to view this page", "danger")
                    return redirect(url_for('auth.login'))
            return view(**kwargs)

        return wrapped_view

    return _wrapper

@bp.route("/account-suspended", methods=["GET"])
def account_suspended():
    if g.user['status_suspend'] is None:
        return redirect(url_for('home.home'))
    else:
        return render_template("auth-engine/suspended.html")


@bp.route("/logout", methods=["GET"])
def logout():
    token = request.form.get("credential")
    if token:
        try:
            id_token.verify_oauth2_token(token, google_requests.Request(),
                                         GOOGLE_CLIENT_ID)
            session.pop("user_id", None)
            return redirect(url_for("home.home"))
        except ValueError:
            # Invalid token
            pass

    session.pop("user_id", None)
    return redirect(url_for("home.home"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if (request.form.get("credential") != None):
            token = request.form.get("credential")
            try:
                user_info = id_token.verify_oauth2_token(token, google_requests.Request(),
                                                         GOOGLE_CLIENT_ID)
                email = user_info.get("email")
                username = user_info.get("given_name")
                db = get_db()
                user = db.execute(
                    'SELECT * FROM user WHERE email_username = ?', (email,)
                ).fetchone()
                if user is None:
                    userid = str(uuid4())
                    db.execute(
                        "INSERT INTO user (id, email_username, password_hash, user_type,display_name) VALUES (?,?,?,?,?)",
                        (userid, email, "", "h__", username), )
                    db.commit()
                    session["user_id"] = userid
                else:
                    session['user_id'] = user['id']
                return redirect(url_for("auth.login"))
            except ValueError:
                pass
        else:
            username = email_is_valid(request.form.get('emailusrname')).email
            password = request.form['password']
            db = get_db()
            error = None

            user = db.execute(
                'SELECT * FROM user WHERE email_username = ?', (username,)
            ).fetchone()
            if user is None:
                error = 'Incorrect username!!'
            elif check_password_hash(user['password_hash'], password) == False:
                error = 'Incorrect password!!'
            if error is None:
                session['user_id'] = user['id']
            else:
                flash(error, "danger")
            return redirect(url_for("auth.login"))
    else:
        if g.user:
            usertype = g.user['user_type']
            flash("Login successful!", "success")
            if 'h' in usertype:
                return redirect(url_for("householder.dashboard"))
            elif 's' in usertype:
                return redirect(url_for("staff.staff"))
            elif 'a' in usertype:
                return redirect(url_for("admin.admin"))
            else:
                abort(400, "Your account has incorrect privileges. Please contact a system administrator.")

        return render_template("./auth-engine/login.html", GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        if (request.form['username'] != ""):
            username = request.form['username']
        
        email = None
        # Validate email
        email_info = email_is_valid(request.form.get('emailaddress'))
        if email_info.is_valid:
            email = email_info.email
        else:
            flash(f"Invalid Email: {email_info.error}", 'danger')
            return render_template("auth-engine/register.html"), 400
        
        password = request.form['password']
        
        db = get_db()

        if db.execute("SELECT * FROM user WHERE email_username == ?", [email, ]).fetchone():
            flash("Another user is already using this e-mail address", 'danger')
            return render_template("auth-engine/register.html"), 400

        error = None
        userid = str(uuid4())
        try:
            if (username != ""):
                db.execute(
                    "INSERT INTO user (id, email_username, password_hash, user_type,display_name) VALUES (?,?,?,?,?)",
                    (userid, email, generate_password_hash(password), "h__", username),
                )
            else:

                db.execute(
                    "INSERT INTO user (id, email_username, password_hash, user_type) VALUES (?,?,?,?)",
                    (userid, email, generate_password_hash(password), "h__"),
                )
            db.commit()
        except db.IntegrityError:
            error = f"Email ID: {email} is already registered."
        else:
            session["user_id"] = userid
            flash("Registration Successful!", "success")
            return redirect(url_for("auth.login"))

    return render_template('./auth-engine/register.html')


@bp.route("/register-staff", methods=["GET", "POST"])
def register_staff():
    # from email_validator import validate_email, EmailNotValidError
    if request.method == 'POST':
        if not request.form.get('emailaddress') \
            or not request.form.get('password'):
            flash("You must provide a valid email and password", 'danger')
            return render_template("auth-engine/register-staff.html"), 400
        
        pwd = request.form.get('password')
        email = None

        # Validate email
        email_info = email_is_valid(request.form.get('emailaddress'))
        if email_info.is_valid:
            email = email_info.email
        else:
            flash(f"Invalid Email: {email_info.error}", 'danger')
            return render_template("auth-engine/register-staff.html"), 400

        # Validate password matching
        if pwd != request.form.get('confirmpassword'):
            flash("Password and Confirm password don't match", 'danger')
            return render_template("auth-engine/register-staff.html"), 400

        display_name = None
        if request.form.get('username'):
            display_name = request.form.get('username')

        db = get_db()

        if db.execute("SELECT * FROM user WHERE email_username == ?", [email, ]).fetchone():
            flash("Another user is already using this e-mail address", 'danger')
            return render_template("auth-engine/register-staff.html"), 400

        staff_suspend_message = " ".join([
            "Staff Application: Your account has been created successfully.",
            "New staff accounts require review and approval from the administrative team.",
            "Please be patient while your new account is being reviewed as part of the registration process.",
            "This may take some time."
        ])

        userid = str(uuid4())

        db.execute(
            "INSERT INTO user (id, email_username, display_name, password_hash, user_type, status_suspend) \
            VALUES (?, ?, ?, ?, '_s_', ?);",
            (userid, email, display_name, generate_password_hash(pwd), staff_suspend_message)
        )
        db.commit()

        session["user_id"] = userid

        return redirect(url_for('staff.staff'))

    else:
        return render_template("auth-engine/register-staff.html")