from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

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
                'price': coverage.price if coverage.price is not None else None
            }

            response_data = {
                'medicine_name': medicine.name,
                'insurance_provider': insurance_provider.name,
                'coverage': coverage_info,
                'cost': {  # Assuming the cost information is to be sent back as a nested dictionary
                    'cost_covered': None,  # Replace these with actual cost covered info if available
                    'cost_not_covered': None  # Replace these with actual cost not covered info if available
                }
            }

            return jsonify(response_data)
        else:
            return jsonify({'error': 'No coverage details found'})
    else:
        return jsonify({'error': 'Invalid medicine or insurance provider'})


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )