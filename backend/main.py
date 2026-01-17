from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="../webapp")

@app.route("/webapp/<path:path>")
def send_webapp(path):
    return send_from_directory(app.static_folder, path)

@app.route("/webapp")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

