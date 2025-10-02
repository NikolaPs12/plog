from flask import Blueprint, render_template, redirect, url_for, flash

from app.forms import RegistrationForm
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

reg = Blueprint('reg', __name__)

@reg.route('/registr', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Aккаунт успешно создан!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка во время регистрации. Пожалуйста повторите попытку.', 'danger')
    return render_template('reg.html', form=form)        