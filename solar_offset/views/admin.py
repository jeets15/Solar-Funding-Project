from flask import Blueprint, render_template, request

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("./admin/admin.html")
