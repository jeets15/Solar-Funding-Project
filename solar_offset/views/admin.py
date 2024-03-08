from flask import Blueprint, render_template, request, session

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET", "POST"])
def admin():
    adminname = session.get('user_id')
    return render_template("./admin/admin.html", adminname=adminname)
