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
    return render_template('post/add_posts.html', form=form)

@post.route('/post_update/<int:id>', methods=['GET', 'POST'])
@login_required
def post_update(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('У вас нет прав на редактирование этого поста.', 'danger')
        return redirect(url_for('main.index'))
    
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        
        try:
            db.session.commit()
            flash('Пост успешно обновлен!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении поста. Пожалуйста, повторите попытку.', 'danger')
    
    return render_template('post/add_posts.html', form=form, post=post)

@post.route('/post_delete/<int:id>', methods=['GET','POST'])
@login_required
def post_delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('У вас нет прав на удаление этого поста.', 'danger')
        return redirect(url_for('main.index'))
    form = PostForm()
    try:
        post.title = form.title.data
        post.content = form.content.data
        db.session.delete(post)
        db.session.commit()
        flash('Пост успешно удален!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении поста. Пожалуйста, повторите попытку.', 'danger')
    
    form.title.data = post.title
    form.content.data = post.content

    return redirect(url_for('main.index'))