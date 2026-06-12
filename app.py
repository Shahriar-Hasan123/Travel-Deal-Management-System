from flask import Flask

app = Flask(__name__)


@app.route("/")
def health():
    return {"msg": "Travel Deal Management System api is running"}


if __name__ == "__main__":
    app.run(debug=True)
