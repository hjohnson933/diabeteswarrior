from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from diabeteswarrior.auth import login_required
from diabeteswarrior.db import get_db

bp = Blueprint("dwarrior", __name__)
bp.config['SECRET_KEY'] = '@@23=SIDE=monday=WIFE=86@@'

@bp.route("/")
def index():
    """Show all the posts, most recent first."""

    db = get_db()
    posts = db.execute("SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC").fetchall()

    return render_template("dwarrior/index.html", posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id. Checks that the id exists and optionally that the current user is the author. To edit the post require the current user to be the author. Raise 404 if a post with the given id doesn't exist or Raise 403 if the current user isn't the author."""

    post = get_db().execute("SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?", (id,),).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",(title, body, g.user["id"]))
            db.commit()
            return redirect(url_for("dwarrior.index"))

    return render_template("dwarrior/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""

    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id))
            db.commit()
            return redirect(url_for("dwarrior.index"))

    return render_template("dwarrior/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post. Ensures that the post exists and that the logged in user is the author of the post. """

    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("dwarrior.index"))
