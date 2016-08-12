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
    return '<h1>This is %s!</h1><p>By the way, you use %s!</p>' % (pagename, user_agent)

@app.route('/user/<username>')
def any_user(username):
    return render_template('user.html', name=username)

"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
@app.route('/app/<anything>')
def anything(anything):
    return '<h1>Not found</h1>', 404

@app.route('/wiki')
def wiki():
    return redirect('http://wikipedia.org')

@app.route('/admin/<name>')
def admin(name):
    if name != 'Yury':
        abort(403)
    return '<h1>You are admin!</h1>'

if __name__ == '__main__':
    manager.run()
