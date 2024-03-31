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

    user_dicts = [ dict(usr) for usr in users ]
    for usr in user_dicts:
        user_types = []
        if "h" in usr["user_type"]:
            user_types.append("Householder")
        if "s" in usr["user_type"]:
            user_types.append("Staff")
        if 'a' in usr['user_type']:
            user_types.append("Admin")
        usr['user_type'] = " & ".join(user_types)

        usr['is_suspended'] = usr['status_suspend'] is not None
        usr['suspend_message'] = usr['status_suspend'] if usr['is_suspended'] else '-'

    return render_template(
        "./users/admin/admin.html",
        users=user_dicts,
    )


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute("DELETE FROM user WHERE id == ?", (user_id,))
    db.commit()
    return redirect('/admin')


@bp.route('/is-suspend-user', methods=['POST'])
def is_suspend_user():
    user_id = request.form['user_id']
    db = get_db()

    if 'suspend_message' in request.form:
        suspend_message = request.form['suspend_message']
        db.execute(
            "UPDATE user SET status_suspend = ? WHERE id == ?",
            (suspend_message, user_id),
        )
    else:
        db.execute(
            "UPDATE user SET status_suspend = ? WHERE id == ?",
            (None, user_id),
        )

    db.commit()
    return redirect('/admin')
