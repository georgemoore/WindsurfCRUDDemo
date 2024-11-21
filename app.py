from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'mysql://root:root@db/crud_demo'
db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    animal_type = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'animal_type': self.animal_type,
            'age': self.age
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([pet.to_dict() for pet in pets])

@app.route('/api/pets', methods=['POST'])
def create_pet():
    data = request.json
    new_pet = Pet(
        name=data['name'],
        animal_type=data['animal_type'],
        age=data['age']
    )
    db.session.add(new_pet)
    db.session.commit()
    return jsonify(new_pet.to_dict()), 201

@app.route('/api/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    pet = Pet.query.get_or_404(id)
    data = request.json
    pet.name = data['name']
    pet.animal_type = data['animal_type']
    pet.age = data['age']
    db.session.commit()
    return jsonify(pet.to_dict())

@app.route('/api/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
