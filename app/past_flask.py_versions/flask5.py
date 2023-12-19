from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from forflaskref import Medicine, InsuranceProvider, Coverage

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)

# Configure Flask app with the database connection string
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define SQLAlchemy models for Medicine and InsuranceProvider
class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class InsuranceProvider(db.Model):
    __tablename__ = 'insurance_providers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Coverage(db.Model):
    __tablename__ = 'coverage'
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, ForeignKey('medicines.id'), nullable=False)
    provider_id = db.Column(db.Integer, ForeignKey('insurance_providers.id'), nullable=False)
    covered = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=True)

# Create your engine and session
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

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

    # Query the database to get medicine and insurance provider details
    medicine = Medicine.query.filter_by(id=medicine_id).first()
    insurance_provider = InsuranceProvider.query.filter_by(id=insurance_provider_id).first()

    if medicine and insurance_provider:
        coverage = Coverage.query.filter_by(medicine_id=medicine_id, provider_id=insurance_provider_id).first()
        if coverage:
            coverage_info = {
                'covered': coverage.covered,
                'price': coverage.price
            }
            return jsonify({
                'medicine_name': medicine.name,
                'insurance_provider': insurance_provider.name,
                'coverage': coverage_info
            })
        else:
            return jsonify({'error': 'No coverage details found'})
    else:
        return jsonify({'error': 'Invalid medicine or insurance provider'})

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
