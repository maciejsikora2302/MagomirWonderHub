from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         if request.form.get('Button1'):
#             message = 'Button 1 Pressed'
#         elif request.form.get('Button2'):
#             message = 'Button 2 Pressed'
#         elif request.form.get('Button3'):
#             message = 'Button 3 Pressed'
#         else:
#             message = 'No button pressed.'
#     elif request.method == 'GET':
#         message = 'Welcome to the website!'
#     return render_template('index.html', message=message)

@app.route('/', methods=['GET', 'POST'])
def home():

    message = "Welcome to Magomir's Wonder Hub!"
    
    return render_template('index.html', message = message, button_count = 3)


if __name__ == '__main__':
    app.run(debug=True, port=23463)
