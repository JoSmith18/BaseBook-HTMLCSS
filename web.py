from flask import Flask, request, session, redirect, render_template
from forms import CreateAccountForm, LoginForm, CommentForm
from data import get_user, all_users

app = Flask(__name__)
app.secret_key = 'THIS!IS!A!TERRIBLE!SECRET!KEY'


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/wall')
    else:
        return render_template('home.html')


@app.route('/users')
def users():
    return render_template('users.html', users=all_users())


@app.route('/account/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('account_create.html', form=CreateAccountForm())
    else:
        form = CreateAccountForm.from_request(request)
        if form.is_valid():
            account = form.create_account()
            session['user_id'] = account['id']
            return redirect(form.success_url)
        else:
            return render_template('account_create.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/wall')
    elif request.method == 'GET':
        return render_template('login.html', form=LoginForm())
    else:
        form = LoginForm.from_request(request)
        if form.is_valid():
            session['user_id'] = form.user_id
            return redirect('/wall')
        else:
            return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/wall')
def wall():
    if 'user_id' in session:
        return render_template('wall.html', user=get_user(session['user_id']))
    else:
        return redirect('/login')


@app.route('/wall/<int:user_id>')
def other_wall(user_id):
    if 'user_id' in session and session['user_id'] == user_id:
        return redirect('/wall')
    user = get_user(user_id)
    if user:
        return render_template('other_wall.html', user=user)
    else:
        return render_template('user_not_found.html'), 404


@app.route('/wall/<int:user_id>/comment', methods=['GET', 'POST'])
def post_comment(user_id):
    if 'user_id' in session:
        current_user = get_user(session['user_id'])
        user = get_user(user_id)
        if user:
            if request.method == 'GET':
                form = CommentForm(wall_owner=user, author=current_user)
                return render_template('wall_comment.html', form=form)
            else:
                form = CommentForm.from_request(
                    request, wall_owner=user, author=current_user)
                if form.is_valid():
                    form.post_comment()
                    return redirect('/wall/{}'.format(user_id))
                else:
                    return render_template('wall_comment.html', form=form)
        else:
            return render_template('user_not_found.html'), 404
    else:
        return redirect('/login')
