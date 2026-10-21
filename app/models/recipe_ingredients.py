from .base import Base
from sqlalchemy import Column,BigInteger,Text,ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship

class RecipeIngredient(Base):
    __tablename__='recipe_ingredient'
    recipe_id=Column(BigInteger,ForeignKey('recipes.recipe_id'),nullable=False)
    ingredient_id=Column(BigInteger,ForeignKey('ingredients.ingredient_id'),nullable=False)
    raw_ingredient_name=Column(Text,nullable=False)
    ingredient_attribute=Column(Text)

    __table_args__=(
        PrimaryKeyConstraint(
            'recipe_id',"ingredient_id",'raw_ingredient_name'
        ),
    )

    recipe=relationship("Recipe",
                        back_populates='recipe_ingredients')
    ingredient=relationship("Ingredients",
                            back_populates='recipe_ingredients')

    