from flask import Blueprint, request, jsonify
from database.models import Medicine, InsuranceProvider, Coverage  # Import your SQLAlchemy models

coverage_bp = Blueprint('coverage', __name__)

# Endpoint to get coverage information for a given medicine and insurance provider
@coverage_bp.route('/api/coverage', methods=['POST'])
def get_coverage():
    data = request.get_json()
    insurance_provider_id = data.get('insurance_provider_id')
    medicine_id = data.get('medicine_id')

    # Query the database to get medicine and insurance provider details
    medicine = Medicine.query.filter_by(id=medicine_id).first()
    insurance_provider = InsuranceProvider.query.filter_by(id=insurance_provider_id).first()

    if medicine and insurance_provider:
        # Fetch coverage details including cost information
        coverage = Coverage.query.filter_by(medicine_id=medicine_id, provider_id=insurance_provider_id).first()

        if coverage:
            coverage_info = {
                'covered': coverage.covered,
                'price': coverage.price if coverage.price is not None else 'Price information unavailable'
            }

            response_data = {
                'medicine_name': medicine.name,
                'insurance_provider': insurance_provider.name,
                'coverage': coverage_info,
                'cost': {
                    'covered': 'Covered' if coverage.covered else 'Not Covered',
                    'cost_covered': coverage.price if coverage.covered else 'Price information unavailable',
                    'cost_not_covered': coverage.price if not coverage.covered else 'Price information unavailable'
                }
            }

            return jsonify(response_data)
        else:
            return jsonify({'error': 'No coverage details found'})
    else:
        return jsonify({'error': 'Invalid medicine or insurance provider'})