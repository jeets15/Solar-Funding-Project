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
    return render_template("./users/admin/admin.html", adminname=adminname, users=user_dicts, is_logged_in=is_logged_in,
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
