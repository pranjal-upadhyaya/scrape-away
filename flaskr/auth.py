from flask import Blueprint, request, g, redirect, url_for, flash, render_template, session

from flaskr.db import get_db

import functools

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        email_id = request.form["emailId"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        if not password:
            error = "Password is required"
        if not first_name:
            error = "First Name is required"
        if not email_id:
            error = "Email is required"

        if not error:
            user = db.execute("select * from user where username = ?", (username,)
                        ,).fetchone()
            if user is None:
                try:
                    db.execute("insert into user(username, password, first_name, last_name, email_id) values (?, ?, ?, ?, ?)", (username, password, first_name, last_name, email_id)
                            ,)
                    db.commit()
                except Exception as e:
                    error = e
                else:
                    return redirect(url_for('auth.login'))
            else:
                error = f"User {username} is already registered"

        flash(error)

    return render_template('auth/register.html')

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        if not password:
            error = "Password is required"

        if not error:
            user = db.execute("select * from user where username = ?", (username,)
                        ,).fetchone()
            if not user:
                error = "Incorrect username"
            elif password != user["password"]:
                error = "Incorrect password"

        if not error:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for('webpage.home'))
            
        g.error = error

    return render_template('auth/login.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_user():
    user_id = session.get("user_id")

    if user_id is None:        
        g.user = None
    else:
        g.user = get_db().execute("select id, username from user where id = ?", (user_id,)).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route("/profile")
@login_required
def profile():
    user_id = session.get("user_id")
    error = None
    try:
        g.user_profile = get_db().execute("select first_name, last_name, email_id, username from user where id = ?", (user_id,)).fetchone()
    except Exception as e:
        redirect(url_for('auth.logout'))
    return render_template('auth/profile.html')

@bp.route("/change_password", methods = ("GET", "POST"))
@login_required
def change_password():
    if request.method == "POST":
        # print("posting")
        data = request.form
        username = data["username"]
        old_password = data["oldPassword"]
        new_password = data["newPassword"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        if not old_password:
            error = "Password is required"
        if not new_password:
            error = "Password is required"

        if not error:
            user = db.execute("select * from user where username = ?", (username,)
                        ,).fetchone()
            if not user:
                error = "Incorrect username"
            elif old_password != user["password"]:
                error = "Incorrect old password"

        if not error:
            try:
                db.execute("update user set password = ? where username = ?", (new_password, username,))
                db.commit()
                return redirect(url_for('auth.logout'))
            except Exception as e:
                error("Failed to change password")
                g.error = error

        g.error = error

    return render_template('auth/change_password.html')