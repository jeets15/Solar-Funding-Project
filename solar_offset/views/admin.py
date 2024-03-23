from flask import Blueprint, render_template, request, redirect, g
from solar_offset.db import get_db
from solar_offset.views.auth import login_required

bp = Blueprint("admin", __name__)


@bp.route("/admin", methods=["GET", "POST"])
@login_required("a")
def admin():
    db = get_db()
    current_admin = g.user['id']
    users = db.execute(
        'SELECT * FROM user WHERE id!= ? ', (current_admin,)
    ).fetchall()
    user_status_list = db.execute('SELECT * FROM user_status ').fetchall()

    user_status_dict = {}
    for user_row in user_status_list:
        user_status_dict[user_row['user_id']] = user_row['suspend']

    user_dicts = []

    for user_row in users:
        user_types = []
        userdict = dict(user_row)
        if "h" in userdict["user_type"]:
            user_types.append("Householder")
        if "s" in userdict["user_type"]:
            user_types.append("Staff")
        if 'a' in userdict['user_type']:
            user_types.append("Admin")

        userdict['user_type'] = " & ".join(user_types)
        userdict["is_suspended"] = user_status_dict.get(user_row['id'], "-")
        user_dicts.append(userdict)
    print(user_dicts)
    return render_template(
        "./users/admin/admin.html",
        users=user_dicts,
    )


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute("DELETE FROM user WHERE id=?", (user_id,))
    db.commit()
    return redirect('/admin')


@bp.route('/is-suspend-user', methods=['POST'])
def is_suspend_user():
    user_id = request.form['user_id']
    db = get_db()
    if 'suspend_message' in request.form:
        suspend_message = request.form['suspend_message']

        db.execute(
            "INSERT INTO user_status (user_id, suspend) VALUES (?,?)", (user_id, suspend_message,)
        )
    else:
        db.execute(
            "DELETE FROM user_status WHERE user_id = ?", (user_id,)
        ).fetchone()

    db.commit()
    return redirect('/admin')
