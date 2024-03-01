from flask import Blueprint, render_template,request

bp = Blueprint("admin", __name__)

@bp.route("/admin",methods=["GET","POST"])
def admin():
    if request.method == "POST":
        userid=request.form["userid"]
        return render_template("./admin/admin.html",userid=userid)