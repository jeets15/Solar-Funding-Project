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
    user_status_list = db.execute('SELECT user_id,flag_suspicious FROM user_status WHERE flag_suspicious=?',
                                  (1,)).fetchall()

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


@bp.route('/flag-user', methods=['POST'])
def flag_user():
    user_id = request.form['user_id']
    db = get_db()
    users = db.execute(
        'SELECT * FROM user_status WHERE user_id = ? ', (user_id,)
    ).fetchone()
    if users is None:
        db.execute(
            "INSERT INTO user_status (user_id, flag_suspicious) VALUES (?,?)",
            (user_id, 1),
        )
    else:
        db.execute(
            "UPDATE user_status SET flag_suspicious = ? WHERE user_id = ?",
            (1, user_id),
        )
    db.commit()
    return redirect('/admin')


@bp.route('/unflag-user', methods=['POST'])
def unflag_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute(
        "UPDATE user_status SET flag_suspicious = ? WHERE user_id = ?",
        (0, user_id),
    )
    db.commit()
    return redirect('/admin')
