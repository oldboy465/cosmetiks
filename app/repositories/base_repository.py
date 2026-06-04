from app import db

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, id):
        return db.session.get(self.model, id)

    def get_all_by_revendedor(self, revendedor_id):
        return self.model.query.filter_by(revendedor_id=revendedor_id).all()

    def get_by_id_and_revendedor(self, id, revendedor_id):
        return self.model.query.filter_by(id=id, revendedor_id=revendedor_id).first()

    def add(self, entity):
        db.session.add(entity)
        return entity

    def delete(self, entity):
        db.session.delete(entity)

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()