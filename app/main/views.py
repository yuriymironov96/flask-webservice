from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, request, abort
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email
from flask.ext.login import login_required

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['ADMIN']:
                send_email(current_app.config['ADMIN'], 'New User', 'mail/new_user', user=user.username)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
    known=session.get('known', False), current_time=datetime.utcnow())

@main.route('/test/<pagename>')
def any_page(pagename):
    user_agent = request.headers.get('User-Agent')
    return render_template('user_agent.html', pagename=pagename, user_agent=user_agent)

@main.route('/user/<username>')
def any_user(username):
    return render_template('user.html', username=username)

@main.route('/app/<anything>')
def anything(anything):
    return render_template('not_found.html')

@main.route('/wiki')
def wiki():
    return redirect('http://wikipedia.org')

@main.route('/admin/<name>')
def admin(name):
    if name != 'Yury':
        abort(403)
    return render_template('admin.html')

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
