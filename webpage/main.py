from flask import Flask, render_template, request
from gw2info import get_gw2_daily, get_gw2_tomorrow
from pprint import pprint
import datetime
app = Flask(__name__)



@app.route('/old', methods=['GET', 'POST'])
def old_home():

    message = "Welcome to Magomir's Wonder Hub!"
    gw2_dailies = get_gw2_daily()
    gw2_tomorrow = get_gw2_tomorrow()
    

    # pprint(gw2_dailies)
    return render_template('index.html', 
                           welcome_message = message, 
                           gw2_dailies = gw2_dailies,
                           gw2_tomorrow = gw2_tomorrow)

@app.route('/', methods=['GET', 'POST'])
def home():

    message = "Welcome to Magomir's Wonder Hub!"
    #counddown should be number of days from today to 10th of next month
    #if today is 10th, countdown should be a string saying "Payday!"
    #if today is after 10th, countdown should be a string saying "Payday in X days"
    today = datetime.datetime.now()
    days_in_month = datetime.datetime(today.year, today.month+1 if today.month!=12 else 1, 1) - datetime.datetime(today.year, today.month, 1)

    days_in_month = days_in_month.days

    if today.day <= 10:
        countdown = 10 - today.day
    else:
        countdown = 10 + (days_in_month - today.day)

    if today.day <= 21:
        countdown_phd = 21 - today.day
    else:
        countdown_phd = 21 + (days_in_month - today.day)

    countdown_text = f"Qualtrics payday in {countdown} days" if countdown != 0 else "Qualtrics payday today!"
    countdown_phd_text = f"PhD payday in {countdown_phd} days" if countdown_phd != 0 else "PhD payday today!"

    def interpolate_color(value, min_value, max_value, start_color, end_color):
        if value < min_value or value > max_value:
            raise ValueError(f"Input value must be between {min_value} and {max_value}")

        # Calculate the interpolation factor based on the input value
        interpolation_factor = (value - min_value) / (max_value - min_value)

        # Calculate the RGB components based on the interpolation factor
        red = int(start_color[0] + interpolation_factor * (end_color[0] - start_color[0]))
        green = int(start_color[1] + interpolation_factor * (end_color[1] - start_color[1]))
        blue = int(start_color[2] + interpolation_factor * (end_color[2] - start_color[2]))

        return red, green, blue

    # Example usage:
    min_value = 0
    max_value = 31
    end_color = (255, 0, 0)  # Red
    start_color = (0, 255, 0)    # Green

    rgb = interpolate_color(countdown, min_value, max_value, start_color, end_color)
    rgb_phd = interpolate_color(countdown_phd, min_value, max_value, start_color, end_color)
    #rgb is gold if value = 0
    rgb = (255, 215, 0) if countdown == 0 else rgb
    rgb_phd = (255, 215, 0) if countdown_phd == 0 else rgb_phd
    

    # pprint(gw2_dailies)
    return render_template('countdown.html',
                            message = message,
                            countdown = countdown_text,
                            countdown_phd = countdown_phd_text,
                            color = {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]},
                            color_phd = {'r': rgb_phd[0], 'g': rgb_phd[1], 'b': rgb_phd[2]})
                        #    welcome_message = message, 
                        #    gw2_dailies = gw2_dailies,
                        #    gw2_tomorrow = gw2_tomorrow)


if __name__ == '__main__':

    app.run(debug=True, port=23463, host='0.0.0.0')
