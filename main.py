# load flask sub-systems
from flask import render_template
from flask.views import MethodView

# load application vars
from public import app
from config.site import defaults #default title


# load page
class Home(MethodView):
    @staticmethod
    def get():
        data = defaults
        data['page'] = {
            'title': 'Home Controller'
        }
        data['meta_description'] = 'Hello there! Welcome to Moodspace.'

        return render_template('home.html', data=data)


app.add_url_rule('/', view_func=Home.as_view('home'))

# testing
@app.route('/') 
def home(): 
	return render_template('home.html')

# run application
if __name__ == '__main__':
	app.run(debug=True)