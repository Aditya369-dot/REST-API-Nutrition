from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def about(station, date):
    temprature = 23
    return {"station": station,
            "date": date,
            "temprature": temprature}

app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)