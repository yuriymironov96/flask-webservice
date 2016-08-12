from flask import Flask, request, redirect
app = Flask(__name__)


@app.route('/')
def homepage():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Homepage!</h1><p>By the way, you use %s!</p>' % user_agent

@app.route('/test/<pagename>')
def any_page(pagename):
    return '<h1>This is %s!</h1>' % pagename

"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
@app.route('/app/<anything>')
def anything(anything):
    return '<h1>Not found</h1>', 404

if __name__ == '__main__':
    app.run(debug=True)
