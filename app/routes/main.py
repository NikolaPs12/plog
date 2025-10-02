from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..extensions import db
from flask_login import login_required, current_user
from ..forms import PostForm
from ..extensions import db
from ..models.posts import Post
from ..models.coments import Coment
from ..forms import CommentForm
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    form = CommentForm()
    
    # Для каждого поста получаем комментарии с пагинацией
    posts_with_comments = []
    for post in posts:
        # Получаем номер страницы для каждого поста из GET параметра
        page = request.args.get(f'page_{post.id}', 1, type=int)
        comments_query = Coment.query.filter_by(post_id=post.id).order_by(Coment.id.desc())
        comments_pagination = comments_query.paginate(
            page=page, 
            per_page=5,  # ⬅️ по 5 комментариев на страницу
            error_out=False
        )
        
        posts_with_comments.append({
            'post': post,
            'comments_pagination': comments_pagination
        })
    
    return render_template('main.html', 
                         posts_with_comments=posts_with_comments, 
                         form=form)

@main.route("/comment/<int:id>", methods=['POST'])
@login_required
def add_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        post = Post.query.get_or_404(id)
        
        new_comment = Coment(
            content=form.content.data, 
            author=current_user, 
            post_id=post.id
        )
        try:
            db.session.add(new_comment)
            db.session.commit()
            flash('Комментарий успешно добавлен!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при добавлении комментария.', 'danger')
    
    return redirect(url_for('main.index'))