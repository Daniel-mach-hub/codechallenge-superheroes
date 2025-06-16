from flask import Blueprint, request, jsonify
from models import db, Hero, Power, HeroPower

bp = Blueprint('api', __name__)

# GET /heroes
@bp.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes])

# GET /heroes/:id
@bp.route('/heroes/<int:id>')
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    return jsonify({"error": "Hero not found"}), 404

# GET /powers
@bp.route('/powers')
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict() for p in powers])

# GET /powers/:id
@bp.route('/powers/<int:id>')
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    return jsonify({"error": "Power not found"}), 404

# PATCH /powers/:id
@bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.json
    if not data.get("description") or len(data["description"]) < 20:
        return jsonify({"errors": ["description must be at least 20 characters"]}), 400

    power.description = data["description"]
    db.session.commit()
    return jsonify(power.to_dict())

# POST /hero_powers
@bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    strength = data.get('strength')
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["strength must be Strong, Weak, or Average"]}), 400

    try:
        hp = HeroPower(
            strength=strength,
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hp)
        db.session.commit()
        return jsonify(hp.to_dict()), 201
    except Exception:
        return jsonify({"errors": ["validation errors"]}), 400
