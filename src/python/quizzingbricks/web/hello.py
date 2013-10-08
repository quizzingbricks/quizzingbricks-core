from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world" 
    #render_template('starter_template.html')

if __name__ == '__main__':
    app.run(debug=True)