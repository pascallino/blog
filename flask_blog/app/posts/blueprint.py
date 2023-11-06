from flask import Blueprint, render_template
from models import *
from flask import request, url_for, redirect
from App import db, app
from .forms import PostForm
from werkzeug.utils import secure_filename
import os

posts = Blueprint('posts', __name__, template_folder="templates")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# routes to /blog
@posts.route('/create', methods=['POST', 'GET'])
def post_create():
    form = PostForm()
    filepath = None
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/static/', filename))
            filepath = filename
        post = Post(title=title, body=body, filepath=filepath)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.post_list'))

    return render_template('posts/post_create.html', form=form)


@posts.route('/')
def post_list():
    i = 0
    q = request.args.get('q')
    if q:
        postlist = Post.query.filter(Post.title.contains(q) |
                                     Post.body.contains(q))
    else:
        postlist  = Post.query.order_by(Post.created.desc())
    return render_template('posts/post_list.html', postlist=postlist, i=i)

#route to specific post details
@posts.route('/<slug>')
def post_details(slug):
    postdetail = Post.query.filter(Post.slug==slug).first()
    return render_template('posts/post_detail.html', postdetail=postdetail)

#route to specific post details
@posts.route('tags/<slug>')
def tag_details(slug):
    i = 0
    tags = Tag.query.filter(Tag.slug==slug).first()
    return render_template('posts/tag_detail.html', tags=tags, i=i)


def save_image(image):
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename  # Return the filename for storing in your database
    return None