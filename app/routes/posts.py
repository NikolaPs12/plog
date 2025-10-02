from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import PostForm
from app.extensions import db
from app.models.posts import Post

post = Blueprint('post', __name__)

@post.route('/add_posts', methods=['GET', 'POST'])
@login_required
def add_posts():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, author=current_user)

        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Пост успешно создан!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании поста. Пожалуйста, повторите попытку.', 'danger')
    return render_template('add_posts.html', form=form)