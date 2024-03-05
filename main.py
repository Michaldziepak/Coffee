from flask import Flask,render_template,url_for
from flask_bootstrap import Bootstrap5
app = Flask(__name__)
Bootstrap5(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/cafes')
def cafes():
    return render_template("cafes.html")

if __name__ == "__main__":
    app.run(debug=True)