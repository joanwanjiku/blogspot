from flask import render_template
from . import main

@main.route('/')
def index():
    title = 'Blog'
    return render_template('main/index.html', title = title)

@main.route('/user/<int:id>')
def profile():
    pass