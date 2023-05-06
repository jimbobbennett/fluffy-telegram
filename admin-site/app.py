from flask import Flask, render_template
import os

# Pangea SDK
from pangea.config import PangeaConfig
from pangea.services import AuthN

PANGEA_TOKEN = os.getenv("PANGEA_AUTHN_TOKEN")
authn_config = PangeaConfig(domain="aws.us.pangea.cloud")

# Setup Pangea AuthN service
authn = AuthN(token=PANGEA_TOKEN, config=authn_config)

authn.Client().login()

# Create a flask app
app = Flask(__name__)

# Create a route
@app.route('/')
def hello_world():
    return render_template("index.html")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

