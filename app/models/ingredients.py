from .base import Base
from sqlalchemy import BigInteger,Column,Text,Identity
from sqlalchemy.orm import relationship

class Ingredients(Base):
    __tablename__='ingredients'
    ingredient_id=Column(BigInteger,Identity(always=True),primary_key=True)
    canonical_name=Column(Text,nullable=False,unique=True)

    names=relationship('AliasNames',
                       back_populates='ingredient',
                       cascade='all,delete-orphan')

    recipe_ingredients=relationship(
        "RecipeIngredient",
        back_populates='ingredient'
    )