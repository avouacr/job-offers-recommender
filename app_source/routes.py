from app_source import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
