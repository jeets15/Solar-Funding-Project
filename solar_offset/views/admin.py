from flask import Blueprint, render_template, request, session, redirect
from solar_offset.db import get_db

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET", "POST"])
def admin():
    adminname = session.get('username')
    db = get_db()
    is_logged_in = True if adminname else False
    if is_logged_in == False:
        return redirect("/login")
    user_types = ["admin", "householder", "staff"]
    print(is_logged_in)
    users = db.execute(
        'SELECT * FROM user WHERE user_type NOT LIKE ? ', ('%a%',)
    ).fetchall()
    user_dicts = []
    for user_row in users:
        userdict = dict(user_row)
        if ("h__" in userdict["user_type"]):
            userdict["user_type"] = "householder"
        else:
            userdict["user_type"] = "staff"
        user_dicts.append(userdict)

    return render_template("./admin/admin.html", adminname=adminname, users=user_dicts, is_logged_in=is_logged_in)


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute("DELETE FROM user WHERE id=?", (user_id,))
    db.commit()
    return redirect('/admin')


@bp.route('/flag-user', methods=['POST'])
def flag_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute(
        "INSERT INTO user_status (user_id, flag_suspicious) VALUES (?,?)",
        (user_id, 1),
    )
    db.commit()
    return redirect('/admin')
