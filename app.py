from flask import Flask, render_template
from main import get_all_articles

app = Flask(__name__)

@app.route("/")
def dashboard():
    articles = get_all_articles()
    return render_template("dashboard.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)
