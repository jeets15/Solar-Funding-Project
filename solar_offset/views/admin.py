from flask import Blueprint, render_template, request, session, redirect
from solar_offset.db import get_db

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        adminname = session.get('username')
        db = get_db()
        users = db.execute(
            'SELECT * FROM user WHERE user_type != ? ', ('admin',)
        ).fetchall()
        return render_template("./admin/admin.html", adminname=adminname, users=users)


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute("DELETE FROM user WHERE id=?", (user_id,))
    db.commit()
    return redirect('/admin')
