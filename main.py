# load flask sub-systems
from flask import Flask,render_template,url_for,request
# from flask.views import MethodView

# load application vars
# from public import app
from config.site import defaults #default title
from reddit_user_api import RedditUserAPI

app = Flask(__name__)

# testing
@app.route('/') 
def home(): 
    data = defaults
    data['page'] = {
        'title': 'Home Controller'
    }
    data['meta_description'] = 'Hello there! Welcome to Moodspace.'
    
    return render_template('home.html', data=data)

# run application
if __name__ == '__main__':
	app.run(debug=True)