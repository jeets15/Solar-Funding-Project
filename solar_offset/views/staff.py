from flask import Blueprint, render_template, request, session

bp = Blueprint("staff", __name__)


@bp.route("/staff", methods=["GET", "POST"])
def staff():
    staffname = session.get('username')
    is_logged_in = True if staffname else False
    return render_template("./users/staff/staffdashboard.html", staffname=staffname, is_logged_in=is_logged_in)
