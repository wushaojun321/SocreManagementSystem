import os
import json
from flask import Flask, request

from libs import validate_github_token

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world4"

@app.route("/deploy", methods=["POST"])
def deploy():
    if not validate_github_token(request.data, request.headers):
        return json.dumps({"msg": "no chance"})
    os.system("sh /home/wsj/ScoreManagementSystem/deploy.sh")
    return json.dumps({"msg": "ok"})

if __name__ == '__main__':
    app.run("0.0.0.0", 8081)
