import random
import string
from google.cloud import firestore

db = firestore.Client.from_service_account_json('./cloud-rangers-fierebase.json')

# Generar un código aleatorio
def generate_code(brand):
    random_digits = ''.join(random.choices(string.digits, k=8))
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    return brand[:2] + random_digits + random_letters

# Crear las 10 entradas en la colección market_appliances
def create_market_appliances():
    types = ["refrigerator", "dishwasher", "washing_machine", "oven"]
    brands = ["BOSH", "LG", "Samsung", "Siemens", "Electrolux"]
    efficiencies = ["A+++", "A++", "A++", "A+", "A+", "A", "A", "B", "C"]
    prices = random.sample(range(100, 1000), 10)  # Generar 10 precios aleatorios
    years = random.choices(range(2018, 2024), k=10)  # Generar 10 años aleatorios

    for _ in range(10):
        appliance = {
            "type": random.choice(types),
            "brand": random.choice(brands),
            "code": generate_code(random.choice(brands)),
            "efficiency": random.choice(efficiencies),
            "price": prices.pop(0),
            "year": years.pop(0)
        }
        db.collection('market_appliances').add(appliance)

# Ejecutar la función para crear las entradas en la colección
create_market_appliances()
