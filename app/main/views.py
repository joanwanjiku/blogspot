from flask import render_template, request, redirect, url_for
from . import main
from .. import photos, db
from ..requests import get_random_quote
from ..models import Post, User, Comment
import datetime
from flask_login import login_required, current_user

@main.route('/', methods=['POST', 'GET'])
def index():
    title = 'Blog'
    quote = get_random_quote()
    posts = Post.get_all_posts()
    comments = ""
    for post in posts:
        
        comments = Comment.get_all_comments(post.id)        
        return render_template('main/index.html', title = title, posts=posts, comments=comments, quote=quote)


@main.route('/user/<int:id>')
@login_required
def profile(id):
    user = User.get_user_by_id(id)
    blog_posts = Post.get_post_by_userid(id)  

    print(user.photo_url)
    return render_template('main/profile.html', user=user, blog_posts=blog_posts)


@main.route('/addpost', methods=['POST', 'GET'])
@login_required
def add_post():
    title='Blog'
    if request.method == 'POST' and 'photo' in request.files:
        print('post')
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']        
        photo_url = photos.save(request.files['photo'])
        path = 'photos/%s' % photo_url
        print(path)
        new_post = Post(title=title, content=content, posted=date, likes=0, dislikes=0, users=current_user, image_url=path)
        new_post.save_post()
        return redirect(url_for('main.index'))
    return render_template('main/index.html', title = title)

@main.route('/post/<int:id>')
def each_post(id):
    post = Post.get_post_by_id(id)

    return render_template('main/post.html', post=post)

@main.route('/post/<int:id>/addcomment', methods=['POST', 'GET'])
def add_comment(id):
    if request.method == 'POST':
        comment = request.form['comment']
        new_comment = Comment(content=comment, post_id=id)
        new_comment.save_comment()
        return redirect(url_for('main.index'))

@main.route('/like/<int:id>')
def like(id):
    post = Post.query.filter_by(id = id).first()
    if post.likes is None:
        post.likes = 0
        post.likes += 1
    else:
        post.likes += 1
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/dislike/<int:id>')
def dislike(id):
    post = Post.query.filter_by(id = id).first()
    if post.dislikes is None:
        post.dislikes = 0
        post.dislikes += 1
    else:
        post.dislikes += 1
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/user/<id>/update/pic', methods=['POST'])
@login_required
def update_pic(id):
    user = User.query.filter_by(id = id).first()
    if 'pr_photo' in request.files:
        filename = photos.save(request.files['pr_photo'])
        path = f'photos/{filename}'
        user.photo_url = path
        db.session.commit()
    return redirect(url_for('main.profile', id=id))

@main.route('/user/<user_id>/comment/delete/<int:id>')
@login_required
def delete(user_id,id):
    comment = Comment.query.filter_by(id=id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('main.profile', id=user_id))