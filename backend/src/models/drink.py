from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
import json

db = SQLAlchemy()


"""
Drink
a persistent drink entity, extends the base SQLAlchemy Model
"""


class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is
    # [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    """
    short()
        short form representation of the Drink model
    """

    def short(self) -> dict:
        short_recipe = [
            {
                "color": r["color"],
                "parts": r["parts"],
            }
            for r in json.loads(self.recipe)
        ]
        return {"id": self.id, "title": self.title, "recipe": short_recipe}

    """
    long()
        long form representation of the Drink model
    """

    def long(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "recipe": json.loads(self.recipe),
        }

    """
    all()
        returns all drinks
    """

    @classmethod
    def all(cls, detail=False) -> list:
        if query := cls.query.all():
            return [d.long() if detail else d.short() for d in query]
        else:
            return None

    """
    find(id)
    find_by(title)
        tries to find a Drink by id or by title
    """

    @classmethod
    def find(cls, id) -> any:
        return cls.query.filter(cls.id == id).one_or_none()

    @classmethod
    def find_by(cls, title) -> any:
        return cls.query.filter(cls.title == title).one_or_none()

    """
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    """

    def update(self):
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
