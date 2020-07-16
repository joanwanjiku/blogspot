from flask import render_template
from . import main
from ..requests import get_random_quote

@main.route('/')
def index():
    title = 'Blog'
    quote = get_random_quote()
    print(quote)
    return render_template('main/index.html', title = title, quote= quote)

@main.route('/user/<int:id>')
def profile():
    pass