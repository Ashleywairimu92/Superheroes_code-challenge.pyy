#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    
    #   In your GET /heroes route
      heroes = Hero.query.all()
      heroes_data = [
    {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        # Ensure hero_powers is not included
    }
    for hero in heroes
]
                      
      return jsonify(heroes_data), 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_heroes_by_id(id):
    heroes = Hero.query.filter_by(id=id).first() 
    #

    if heroes :
        heroes =heroes.to_dict()
        hero_powers = HeroPower.query.filter_by(hero_id=id).all()
        heroes['hero_powers'] = [hero_power.to_dict() for hero_power in hero_powers]
        return  heroes, 200
    else:
        return {'error': 'Hero not found'}, 404
    
       
@app.route('/powers', methods = ['GET'])
def get_all_powers():
       
      powers = Power.query.all()
      powers_data = [
    {
        "id": power.id,
        "name": power.name,
        "description": power.description,
        # Ensure hero_powers is not included
    }
    for power in powers
]

      return jsonify(powers_data), 200
@app.route('/powers/<int:id>', methods=['GET'])
def get_powers_by_id(id):
    power = Power.query.get(id)
    if power:
        return make_response(power.to_dict(), 200)
    else:
        return make_response({"error": "Power not found"}, 404)  
      
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_powers(id):
    power = Power.query.get(id)
    if not power:
        return make_response({"error": "Power not found"}, 404)
    
    try:
        if 'description' in request.json:
            power.description = request.json['description']  # This may raise ValueError
        db.session.commit()
        return make_response(power.to_dict(), 200)
    except ValueError as e:
        return make_response({"errors": ["validation errors"]}, 400)

@app.route('/hero_powers', methods=['POST'])
def post_hero_powers():
    data = request.get_json()
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 200  # Replace with your dict method
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500            

if __name__ == '__main__':
    app.run(port=5555, debug=True)
