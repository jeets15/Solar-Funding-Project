from flask import Blueprint, render_template, request, session, redirect

bp = Blueprint("staff", __name__)


@bp.route("/staff", methods=["GET", "POST"])
def staff():
    staffname = session.get('username')
    is_logged_in = True if staffname else False
    if is_logged_in == False:
        return redirect("/login")
    return render_template("./staff/staffdashboard.html", staffname=staffname, is_logged_in=is_logged_in)
