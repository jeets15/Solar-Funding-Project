from flask import Blueprint, render_template, request, session

bp = Blueprint("staff", __name__)


@bp.route("/staff", methods=["GET", "POST"])
def staff():
    staffname = session.get('username')
    return render_template("./staff/staffdashboard.html", staffname=staffname)
