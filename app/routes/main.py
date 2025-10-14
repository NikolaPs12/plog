from flask import Blueprint, render_template, flash, request, redirect, url_for
from ..extensions import db, cache
from flask_login import login_required, current_user
from ..extensions import db
from ..models.posts import Post
from ..models.coments import Coment
from ..models.user import User
from ..forms import CommentForm, SearchForm, FilterForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Можно перенаправлять на /posts, если хочешь, чтобы главная была страница с постами
    return redirect(url_for('main.index'))

@main.route('/posts', methods=['GET', 'POST'])
def index():
    filter_form = FilterForm()
    filter_form.author.choices = [(0, '👥 Все авторы')] + [
        (user.id, user.username) for user in User.query.all()
    ]
    
    # ⬇️ ИСПРАВЛЕНО: получаем параметры фильтрации
    author_id = request.args.get('author', type=int)  # ⬅️ было 'author_id'
    sort_by = request.args.get('sort_by', 'newest')
    page_post = request.args.get('page_post', 1, type=int)
    search_query = request.args.get('q', '')
    
    # Формы
    form = CommentForm()
    search_form = SearchForm()
    
    # БАЗОВЫЙ ЗАПРОС
    posts_query = Post.query
    
    # ⬇️ ИСПРАВЛЕНО: применяем фильтрацию по автору
    if author_id and author_id != 0:  # ⬅️ проверяем что не "Все авторы"
        posts_query = posts_query.filter_by(author_id=author_id)

    # ⬇️ ИСПРАВЛЕНО: применяем сортировку
    if sort_by == 'newest':
        posts_query = posts_query.order_by(Post.id.desc())
    elif sort_by == 'oldest':
        posts_query = posts_query.order_by(Post.id.asc())
    elif sort_by == 'popular':
        posts_query = posts_query.outerjoin(Coment).group_by(Post.id).order_by(db.func.count(Coment.id).desc())
    
    # ⬇️ ИСПРАВЛЕНО: применяем поиск (должно быть после фильтрации)
    if search_query:
        posts_query = posts_query.filter(
            Post.title.ilike(f'%{search_query}%') | 
            Post.content.ilike(f'%{search_query}%')
        )
    
    # ⬇️ ИСПРАВЛЕНО: пагинация применяется к отфильтрованному запросу
    posts_pagination = posts_query.paginate(
        page=page_post, 
        per_page=3,
        error_out=False
    )
    
    # Для каждого поста получаем комментарии с пагинацией
    posts_with_comments = []
    for post in posts_pagination.items: 
        comment_page = request.args.get(f'page_{post.id}', 1, type=int)
        comments_pagination = Coment.query.filter_by(post_id=post.id)\
                                        .order_by(Coment.id.desc())\
                                        .paginate(
                                            page=comment_page,
                                            per_page=5,
                                            error_out=False
                                        )
        
        posts_with_comments.append({
            'post': post,
            'comments_pagination': comments_pagination
        })
    
    return render_template('base/main.html',
                         posts_with_comments=posts_with_comments, 
                         posts_pagination=posts_pagination, 
                         form=form,
                         search_form=search_form,
                         search_query=search_query,
                         current_author=author_id, 
                         current_sort=sort_by,
                         filter_form=filter_form)


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


