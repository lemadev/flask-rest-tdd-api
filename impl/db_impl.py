from app import db

def save(instance):
    db.session.add(instance)
    db.session.commit()

def delete(instance):
    db.session.delete(instance)
    db.session.commit()

