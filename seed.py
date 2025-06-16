from app import app
from models import db, Hero, Power

with app.app_context():
    db.drop_all()
    db.create_all()

    h1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    p1 = Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed")

    db.session.add_all([h1, p1])
    db.session.commit()
