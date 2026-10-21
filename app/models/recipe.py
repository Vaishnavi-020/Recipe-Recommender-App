from .base import Base
from sqlalchemy import Column,Integer,BigInteger,Text
from sqlalchemy.orm import relationship

class Recipe(Base):
    __tablename__='recipes'
    recipe_id=Column(BigInteger,primary_key=True)
    recipe_title=Column(Text,nullable=False)
    cuisine=Column(Text)
    instructions=Column(Text)
    total_time_minutes=Column(Integer)
    ingredient_count=Column(Integer)
    url=Column(Text)
    image_url=Column(Text)

    recipe_ingredients=relationship("RecipeIngredient",
                                    back_populates='recipe')
    