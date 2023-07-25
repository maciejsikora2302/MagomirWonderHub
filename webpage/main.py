from flask import Flask, render_template, request
from gw2info import get_gw2_daily, get_gw2_tomorrow
from pprint import pprint
app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def home():

    message = "Welcome to Magomir's Wonder Hub!"
    gw2_dailies = get_gw2_daily()
    gw2_tomorrow = get_gw2_tomorrow()
    

    # pprint(gw2_dailies)
    return render_template('index.html', 
                           welcome_message = message, 
                           gw2_dailies = gw2_dailies,
                           gw2_tomorrow = gw2_tomorrow)




if __name__ == '__main__':

    app.run(debug=True, port=23463, host='0.0.0.0')
