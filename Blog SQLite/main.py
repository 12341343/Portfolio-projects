from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor, CKEditorField
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['CKEDITOR_PKG_TYPE'] = 'Full'
db = SQLAlchemy()
db.init_app(app)
ckeditor = CKEditor()
ckeditor.init_app(app)


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField('Body')
    submit = SubmitField("Submit Post")


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    post = db.session.execute(db.select(BlogPost)).scalars()
    posts = post.all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["POST", "GET"])
def add_new_post():
    form = CreatePostForm()
    x = datetime.now()
    heading_source = "New Post"
    if form.validate_on_submit():
        new_post = BlogPost(
            title=request.form['title'],
            date=x.strftime("%B %d, %Y"),
            body=request.form['body'],
            author=request.form["author"],
            img_url=request.form['img_url'],
            subtitle=request.form['subtitle']
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form, heading_source=heading_source)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    heading_source = "Edit Post"
    form = CreatePostForm()
    if request.method == "GET":
        requested_post = db.get_or_404(BlogPost, post_id)
        form.title.data = requested_post.title
        form.body.data = requested_post.body
        form.author.data = requested_post.author
        form.img_url.data = requested_post.img_url
        form.subtitle.data = requested_post.subtitle
    if form.validate_on_submit():
        seleceted_bp = db.get_or_404(BlogPost, post_id)
        if seleceted_bp:
            seleceted_bp.title = request.form['title']
            seleceted_bp.body = request.form['body']
            seleceted_bp.author = request.form["author"]
            seleceted_bp.img_url = request.form['img_url']
            seleceted_bp.subtitle = request.form['subtitle']
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))

    return render_template("make-post.html", heading_source=heading_source, form=form)


# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<int:post_id>', methods=["GET", "POST"])
def delete_post(post_id):
    if request.method == "GET":
        find_post = db.get_or_404(BlogPost, post_id)
        if find_post:
            db.session.delete(find_post)
            db.session.commit()
            return redirect(url_for('get_all_posts'))
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
