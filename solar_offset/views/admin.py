from flask import Blueprint, render_template, request, session, redirect
from solar_offset.db import get_db
from solar_offset.views.auth import login_required

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET", "POST"])
@login_required("a")
def admin():
    db = get_db()
    user_types = ["admin", "householder", "staff"]
    users = db.execute(
        'SELECT * FROM user WHERE user_type NOT LIKE ? ', ('%a%',)
    ).fetchall()
    user_status_list = db.execute('SELECT * FROM user_status ').fetchall()

    user_status_dict = []
    for user_row in user_status_list:
        userstatusdict = dict(user_row)
        user_status_dict.append(userstatusdict)

    user_dicts = []
    for user_row in users:
        userdict = dict(user_row)
        if ("h__" in userdict["user_type"]):
            userdict["user_type"] = "householder"
        else:
            userdict["user_type"] = "staff"
        user_dicts.append(userdict)

        user_statuses = [item['user_id'] for item in user_status_dict]
    return render_template(
        "./users/admin/admin.html",
        users=user_dicts,
        user_status_list=user_statuses)


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute("DELETE FROM user WHERE id=?", (user_id,))
    db.commit()
    return redirect('/admin')


@bp.route('/suspend-user', methods=['POST'])
def suspend_user():
    suspend_message = request.form['suspend_message']
    user_id = request.form['user_id']
    db = get_db()
    db.execute(
        "INSERT INTO user_status (user_id, suspend) VALUES (?,?)", (user_id, suspend_message,)
    )
    db.commit()
    return redirect('/admin')


@bp.route('/unsuspend-user', methods=['POST'])
def unsuspend_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute(
        "DELETE FROM user_status WHERE user_id = ?", (user_id,)
    ).fetchone()
    db.commit()
    return redirect('/admin')
