from flask import Flask, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from data.users import User
from data import db_session
import datetime
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "N#pC@UzmS5kw%@$F"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)

#  Инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Получение текущего пользователся"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/register", methods=["GET", "POST"])
def reqister():
    """Форма регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Registration",
                form=form,
                message="Passwords do not match",
            )
        db_sess = db_session.create_session()

        all_users = db_sess.query(User.name).all()
        if not all([form.name.data != user_name[0] for user_name in all_users]):
            return render_template(
                "register.html",
                form=form,
                message="There is already a user with the same name",
            )

        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template(
                "register.html", form=form, message="This user already exists"
            )
        user = User(
            name=form.name.data,
            status="Пользователь",
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        return redirect("/book")
    return render_template("register.html", title="Registration", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Форма авторизации"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/book")
        return render_template(
            "login.html", message="Incorrect login or password", form=form
        )
    return render_template("login.html", title="Authorization", form=form)


@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return render_template("book_view.html")
    return render_template("homepage.html")


@app.route("/book")
@login_required
def book():
    return render_template("book_view.html")


@app.errorhandler(401)
def unauthorized(error):
    """Пользователь не авторизован"""
    return redirect("/register")


@app.errorhandler(404)
def not_found(error):
    """Страница не найдена"""
    return render_template("errors/404.html")


@app.route("/logout")
@login_required
def logout():
    """Выход из учётной записи"""
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("db/data.db")
    app.run(port=8080, host="127.0.0.1")
