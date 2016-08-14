from flask import Flask, request, redirect, abort, render_template
from flask.ext.script import Manager

app = Flask(__name__)
manager =  Manager(app)

@app.route('/')
def homepage():
    return render_template('index.html')

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

if __name__ == '__main__':
    manager.run()
