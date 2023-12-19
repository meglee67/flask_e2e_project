from flask import Flask, render_template, url_for, redirect, session, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from dotenv import load_dotenv
from db_functions import update_or_create_user
import os
import sentry_sdk

sentry_sdk.init(
    dsn="https://c402dd2e87b4232687da099038d06895@o4506420135723008.ingest.sentry.io/4506420136837120",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

load_dotenv()

# OAuth initialization
oauth = OAuth(app)

DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)

app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost_covered = db.Column(db.Float, nullable=False)
    cost_not_covered = db.Column(db.Float, nullable=False)


class InsuranceProvider(db.Model):
    __tablename__ = 'insurance_providers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Coverage(db.Model):
    __tablename__ = 'coverage'
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('insurance_providers.id'), nullable=False)
    covered = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=True)


@app.route('/')
def index():
    return render_template('index.html')


# OAuth routes...
# ...


@app.route('/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    medicine_list = [{'id': med.id, 'name': med.name} for med in medicines]
    return jsonify({'medicines': medicine_list})


@app.route('/insurance-providers', methods=['GET'])
def get_insurance_providers():
    providers = InsuranceProvider.query.all()
    provider_list = [{'id': prov.id, 'name': prov.name} for prov in providers]
    return jsonify({'insurance_providers': provider_list})


@app.route('/medicine-info', methods=['POST'])
def get_medicine_info():
    data = request.get_json()
    insurance_provider_id = data.get('insurance_provider_id')
    medicine_id = data.get('medicine_id')

    # Query the database to get medicine and insurance provider details...

# Blueprint for coverage API
coverage_bp = Blueprint('coverage', __name__)

@coverage_bp.route('/coverage-info')
def coverage_info():
    # Logic for coverage information
    return 'Coverage Information'

# Register Blueprint within Flask app
app.register_blueprint(coverage_bp, url_prefix= '/coverage')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
