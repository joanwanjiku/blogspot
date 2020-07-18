from flask import render_template, request, redirect, url_for
from . import main
from .. import photos
from ..requests import get_random_quote
from ..models import Post, User, Comment
import datetime
from flask_login import login_required, current_user

@main.route('/', methods=['POST', 'GET'])
def index():
    title = 'Blog'
    # quote = get_random_quote()
    posts = Post.get_all_posts()
    comments = ""
    for post in posts:
        print(post.id)
        comments = Comment.get_all_comments(post.id)
        print(comments[0].content)
        return render_template('main/index.html', title = title, posts=posts, comments=comments)

@main.route('/user/<int:id>')
@login_required
def profile(id):
    user = User.get_user_by_id(id)
    return render_template('main/profile.html', user=user)


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

