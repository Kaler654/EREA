from flask import Flask, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from forms.register_form import RegisterForm
from data.users import User
from data import db_session
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'N#pC@UzmS5kw%@$F'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """Форма регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()

        all_users = db_sess.query(User.name).all()
        if not all([form.name.data != user_name[0] for user_name in all_users]):
            return render_template('register.html', form=form,
                                   message="Пользователь с таким именем уже есть")

        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            status="Пользователь",
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
@app.route('/index')
def index():
    return render_template("homepage.html")


if __name__ == '__main__':
    db_session.global_init("db/data.db")
    app.run(port=8080, host='127.0.0.1')
