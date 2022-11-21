from flask import Flask, render_template, url_for, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from data.users import User
from data import db_session
import datetime
import os
from flask_login import LoginManager
import translators as ts
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "N#pC@UzmS5kw%@$F"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)

#  Инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


def translate_js(word):
    word = str(word)
    return ts.google(word, from_language='tt', to_language='ru')


@app.route("/get_translate", methods=["POST"])
def get_translate():
    text = json.loads(request.data)["text"]
    print(text)
    # select_text = request.form.get("selectText")
    # return jsonify({"translateText": translate_test(select_text)})
    return json.dumps({"translate": translate_js(text)})


def add_word_to_dict(w):  # принимает татарское слово
    db_sess = db_session.create_session()
    word_id = db_sess.query(Words.id).filter(Words.word_tat == w.lower()).first()
    if not word_id:
        new_word = Words()
        new_word.word_tat = w.lower()
        new_word.word_ru = translate_tat_to_rus(w.lower())
        db_sess.add(new_word)
        db_sess.commit()
    word_id = db_sess.query(Words.id).filter(Words.word_tat == w.lower()).first()[0]
    new_ass = Users_to_words()
    new_ass.word_id = word_id
    new_ass.user_id = current_user.id
    try:
        db_sess.add(new_ass)
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        pass


def delete_word_of_dict(w):  # принимает татарское слово
    db_sess = db_session.create_session()
    word_id = db_sess.query(Words.id).filter(Words.word_tat == w.lower()).first()
    if word_id:
        word = db_sess.query(Words).filter(Words.id == word_id[0]).first()
        ass = db_sess.query(Users_to_words).filter(Users_to_words.user_id == current_user.id,
                                                   Users_to_words.word_id == word_id[0]).first()
        db_sess.delete(word)
        db_sess.delete(ass)
        db_sess.commit()


@app.route("/add_wordToDict", methods=["POST"])
def add_word_post():
    word = json.loads(request.data)["word"]
    print(word)
    add_word_to_dict(word)
    return json.dumps({'success': True})


@app.route("/remove_wordFromDict", methods=["POST"])
def remove_word_post():
    word = json.loads(request.data)["word"]
    print(word)
    delete_word_of_dict(word)
    return json.dumps({'success': True})


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
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=8080, host="127.0.0.1")
