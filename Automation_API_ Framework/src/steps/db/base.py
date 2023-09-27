from sqlalchemy import asc, desc


class Registry(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls


class BaseDbSteps(metaclass=Registry):
    model = None
    name: str = None

    def __init__(self, db_client):
        self.db_client = db_client

    def create(self, **kwargs):
        return self.model.create(**kwargs)

    def delete_all(self):
        self.model.query.delete()

    def get_model(self):
        return self.model

    def refresh(self, inst):
        self.db_client.session.refresh(inst)

    def update(self, inst, **param):
        inst.update(**param)

    def get_first(self, **kwargs):
        return self.model.where(**kwargs).first()

    def get_one(self, **kwargs):
        return self.model.where(**kwargs).one()

    def get_all_filtered(self, **kwargs):
        return self.db_client.session.query(self.model).filter(
            *[getattr(self.model, k) == v for k, v in kwargs.items()]).all()

    def get_all(self, **kwargs):
        return self.model.where(**kwargs).all()

    def get_sorted(self, field, sort_type):
        ordering_func = {
            'ASC': asc,
            'DESC': desc
        }.get(sort_type)
        result = self.db_client.session.query(self.model).order_by(ordering_func(field)).all()
        return result
