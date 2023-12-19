from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from faker import Faker
import os
import random 
from dotenv import load_dotenv
from table_creation import Medicine, InsuranceProvider, Coverage

load_dotenv()

## Database credentials 
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string and creating the engine 
connect_args={'ssl':{'fake_flag_to_enable_tls': True}}
connection_string = (f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
                    f"?charset={DB_CHARSET}")

engine = create_engine(
        connection_string,
        connect_args=connect_args)

# Creating a session to populate the data
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# Medicines and their costs when covered and not covered by insurance
medicines_data = [
    {"name": "Metformin", "cost_covered": 2, "cost_not_covered": 10},
    {"name": "Adderall", "cost_covered": 25, "cost_not_covered": 40},
    {"name": "Ozempic", "cost_covered": 25, "cost_not_covered": 900},
    {"name": "Wegovy", "cost_covered": 270, "cost_not_covered": 1350},
    {"name": "Lisinopril", "cost_covered": 3, "cost_not_covered": 30}
]

# Add medicines to the database
for med_data in medicines_data:
    medicine = Medicine(
        name=med_data["name"],
        cost_covered=med_data["cost_covered"],
        cost_not_covered=med_data["cost_not_covered"]
    )
    session.add(medicine)

    # Insurance providers and the medicines they cover
insurance_providers_data = [
    {
        "name": "Empire Blue Cross Blue Shield",
        "coverages": {
            "Metformin": True,
            "Adderall": True,
            "Ozempic": True,
            "Wegovy": False,
            "Lisinopril": True
        }
    },
    {
        "name": "Aetna",
        "coverages": {
            "Metformin": True,
            "Adderall": False,
            "Ozempic": False,
            "Wegovy": False,
            "Lisinopril": True
        }
    },
    {
        "name": "Humana",
        "coverages": {
            "Metformin": False,
            "Adderall": True,
            "Ozempic": True,
            "Wegovy": False,
            "Lisinopril": False
        }
    },
    {
        "name": "United",
        "coverages": {
            "Metformin": False,
            "Adderall": False,
            "Ozempic": True,
            "Wegovy": True,
            "Lisinopril": False
        }
    }
]

# Add insurance providers to the database
for provider_data in insurance_providers_data:
    provider = InsuranceProvider(name=provider_data["name"])
    session.add(provider)
    for med_name, covered in provider_data["coverages"].items():
        medicine = session.query(Medicine).filter_by(name=med_name).first()
        if medicine:
            coverage = Coverage(
                medicine_id=medicine.id,
                provider_id=provider.id,
                covered=covered,
                price=medicine.cost_covered if covered else medicine.cost_not_covered
            )
            session.add(coverage)

# Commit the changes to the database for insurance providers and coverage
session.commit()

# Close the session for insurance providers and coverage
session.close()