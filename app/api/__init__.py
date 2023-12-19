from flask import Flask
from app.api.coverage import coverage_bp  # Import your API blueprint

app = Flask(__name__)

# Other configurations and app setup...

# Register API blueprints
app.register_blueprint(coverage_bp, url_prefix='/')  # Adjust the URL prefix as needed

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )

