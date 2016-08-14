import os
from flask import Flask, request, redirect, abort, render_template, session, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
db = SQLAlchemy(app)
manager =  Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('homepage'))
    return render_template('index.html', form=form, name=session.get('name'),
    known=session.get('known', False), current_time=datetime.utcnow())

@app.route('/test/<pagename>')
def any_page(pagename):
    user_agent = request.headers.get('User-Agent')
    return render_template('user_agent.html', pagename=pagename, user_agent=user_agent)

@app.route('/user/<username>')
def any_user(username):
    return render_template('user.html', username=username)

@app.route('/app/<anything>')
def anything(anything):
    return render_template('not_found.html')

@app.route('/wiki')
def wiki():
    return redirect('http://wikipedia.org')

@app.route('/admin/<name>')
def admin(name):
    if name != 'Yury':
        abort(403)
    return render_template('admin.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
