from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    

class InsuranceProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    

# Create a route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Create a route for selecting medicines
@app.route('/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    medicine_list = [{'id': med.id, 'name': med.name} for med in medicines]
    return jsonify({'medicines': medicine_list})

# Create a route for selecting insurance providers
@app.route('/insurance-providers', methods=['GET'])
def get_insurance_providers():
    providers = InsuranceProvider.query.all()
    provider_list = [{'id': prov.id, 'name': prov.name} for prov in providers]
    return jsonify({'insurance_providers': provider_list})

# Create a route for handling selected insurance provider and medicine
@app.route('/medicine-info', methods=['POST'])
def get_medicine_info():
    data = request.get_json()
    insurance_provider_id = data.get('insurance_provider_id')
    medicine_id = data.get('medicine_id')

    medicine = Medicine.query.get(medicine_id)
    insurance_provider = InsuranceProvider.query.get(insurance_provider_id)

    # Process data, check coverage, calculate cost, etc.
    # Sample response, modify as needed
    if medicine and insurance_provider:
        return jsonify({
            'medicine_name': medicine.name,
            'insurance_provider': insurance_provider.name,
            'coverage': 'Sample coverage information',
            'cost': 'Sample cost information'
        })
    else:
        return jsonify({'error': 'Invalid medicine or insurance provider'})

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
