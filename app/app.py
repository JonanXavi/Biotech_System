from flask import Flask, render_template

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/recover")
def recover():
    return render_template('password.html')

if __name__=='__main__':
    app.run(debug=True, port='5000')