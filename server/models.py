from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Hero Model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String, nullable=False)
    

    hero_powers = db.relationship('HeroPower', back_populates='hero')

 
    powers = association_proxy('hero_powers', 'power')

  
    serialize_rules = ('-hero_powers.hero',)

    def __repr__(self):
        return f'<Hero {self.id}: {self.name}>'

# Power Model
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

  
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete')

 
    heroes = association_proxy('hero_powers', 'hero')

 
    serialize_rules = ('-hero_powers.power',)


    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

    def to_dict(self, include_hero_powers=False):
        power_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
        if include_hero_powers:
            power_dict["hero_powers"] = [hero_power.to_dict() for hero_power in self.hero_powers]
        return power_dict


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    
   
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')


    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')


    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("validation errors")
        return value

    def __repr__(self):
        return f'<HeroPower {self.id}: Hero {self.hero_id} Power {self.power_id}>'

