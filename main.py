# load flask sub-systems
from flask import Flask,render_template,url_for,request
# from flask.views import MethodView

# load application vars
# from public import app
from config.site import defaults #default title
from reddit_user_api import *
from graph_api import *

app = Flask(__name__)

# testing
@app.route('/') 
def home(): 
    data = defaults
    data['page'] = {
        'title': 'Home'
    }
    data['meta_description'] = 'Hello there! Welcome to Moodspace.'
    
    return render_template('home.html', data=data)

@app.route('/prediction_user/',methods=['POST', 'GET']) # @app.route('/index',methods=['POST'])
def prediction_user(): # def post_submit():
    if request.method == 'POST':
        username = request.form['username']
    user_obj = RedditUserAPI(username)

    # 
    clean_data = user_obj.get_clean_data()
    pred_df = user_obj.get_prediction(clean_data)

    # 
    month_cat_df = user_obj.get_df_by_month_and_cat(pred_df)
    month_df = user_obj.get_df_by_month(pred_df) 

    #
    total_post = pred_df.shape[0]
    num_neg_post = len(pred_df[pred_df['class'] == 1])
    neg_precent_int = int(num_neg_post/total_post * 100)
    if neg_precent_int > 50:
        sentiment = 'negative'
    else:
        sentiment = 'positive'
    neg_percent = str(int(num_neg_post/total_post * 100)) + '%'
    # ret_dict = {'total_post': total_post, 'num_neg_post': num_neg_post, 'neg_precent': neg_precent}


    # graph
    line_graph_json = CreateGraph().get_line_graph(month_df)
    bar_graph_json = CreateGraph().get_bar_graph(pred_df)
    stacked_bar_graph_json = CreateGraph().get_stacked_bar_graph(month_cat_df)


    return render_template('prediction_user.html', 
                            line_graph_json=line_graph_json, stacked_bar_graph_json=stacked_bar_graph_json, bar_graph_json=bar_graph_json,
                            username=username, total_post=total_post, sentiment=sentiment, neg_percent=neg_percent)

@app.route('/prediction_solo/',methods=['POST', 'GET']) # @app.route('/index',methods=['POST'])
def prediction_user(): # def post_submit():
    return render_template('prediction_solo.html')


# run application
if __name__ == '__main__':
	app.run(debug=True)