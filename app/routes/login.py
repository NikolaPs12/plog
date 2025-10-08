from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app.forms import LoginForm
from app.forms import ResetPasswordForm , ForgotPasswordForm
from app.models.user import User
from app.extensions import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from itsdangerous import URLSafeTimedSerializer 
from ..models.user import User
from ..extensions import db, login_manager
from flask_mail import Message
from ..extensions import mail
from werkzeug.security import generate_password_hash

login = Blueprint('login', __name__)



@login.route('/login', methods=['POST', 'GET'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Неверный email или пароль.', 'danger')  
    return render_template('log/login.html', form=form)

@login.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = s.dumps(user.email, salt='password-reset-salt')
            result_link = url_for('login.reset_password', token=token, _external=True)
            msg = Message('Сброс пароля',
                            sender=current_app.config['MAIL_USERNAME'], 
                            recipients=[user.email])
            msg.body = f'Чтобы сбросить пароль, перейдите по следующей ссылке: {result_link}'
            mail.send(msg)
            flash('Письмо для сброса пароля отправлено на ваш email.', 'info')
            return redirect(url_for('login.login_view'))
        else:
            flash('Пользователь с таким email не найден.', 'warning')
            return redirect(url_for('login.forgot_password'))
    
    return render_template('log/forgot_password.html', form=form)

@login.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # токен действителен 1 час
    except:
        flash('Ссылка для сброса пароля недействительна или истекла.', 'danger')
        return redirect(url_for('login.forgot_password'))    

    user = User.query.filter_by(email=email).first()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был успешно сброшен. Теперь вы можете войти с новым паролем.', 'success')
        return redirect(url_for('login.login_view'))
    return render_template('log/reset_password.html', form=form)

@login.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('main.index'))