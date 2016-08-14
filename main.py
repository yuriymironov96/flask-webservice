from flask import Flask, request, redirect, abort, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime

app = Flask(__name__)
manager =  Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def homepage():
    return render_template('index.html', current_time=datetime.utcnow())

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
