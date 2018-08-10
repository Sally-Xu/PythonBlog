from app import db
from models import Post
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_required, current_user
from posts.forms import PostForm

from datetime import datetime

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()

        flash("Your post is saved!", "success")
        return redirect(url_for('main.home'))

    return render_template('editpost.html', title = 'New Post', legend='New Post', form = form)

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post = post)

@posts.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():   
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = datetime.utcnow()
        db.session.commit()
        flash("Your post has been updated saved!", "success")
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('editpost.html', title = 'Edit Post', legend='Update Post', form = form)

@posts.route("/post/<int:post_id>/del", methods=['POST'])
@login_required
def del_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for('main.home'))