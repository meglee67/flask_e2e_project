# this is the flask app that attempts to integrate Google OAuth

from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from dotenv import load_dotenv
from db_functions import update_or_create_user
import os
import sentry_sdk
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from forflaskref import Medicine, InsuranceProvider, Coverage

sentry_sdk.init(
    dsn="https://c402dd2e87b4232687da099038d06895@o4506420135723008.ingest.sentry.io/4506420136837120",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

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
def main_index():
    return render_template('index.html')

# beginning of OAuth stuff

@app.route('/oauthindex')
def oauth_index():
    return render_template('oauthindex.html')

@app.route('/google/')
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    ###note, if running locally on a non-google shell, do not need to override redirect_uri
    ### and can just use url_for as below
    redirect_uri = url_for('google_auth', _external=True)
    print('REDIRECT URL: ', redirect_uri)
    session['nonce'] = generate_token()
    ##, note: if running in google shell, need to override redirect_uri 
    ## to the external web address of the shell, e.g.,
    # redirect_uri = 'https://5000-cs-213132341638-default.cs-us-east1-pkhd.cloudshell.dev/google/auth/'
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    update_or_create_user(user)
    print(" Google User ", user)
    return redirect('/oauthloginpage')

@app.route('/oauthloginpage/')
def dashboard():
    user = session.get('user')
    if user:
        return render_template('oauthloginpage.html', user=user)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# end of OAuth stuff

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





if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )