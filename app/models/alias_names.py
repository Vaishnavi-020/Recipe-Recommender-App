from .base import Base
from sqlalchemy import Column,BigInteger,Text,ForeignKey,Identity,CheckConstraint
from sqlalchemy.orm import relationship

class AliasNames(Base):
    __tablename__='alias_names'
    alias_id=Column(BigInteger,Identity(always=True),primary_key=True)
    ingredient_id=Column(BigInteger,ForeignKey('ingredients.ingredient_id'),nullable=False)
    alias_name=Column(Text,nullable=False,unique=True)
    

    ingredient=relationship(
        'Ingredients',
        back_populates='names'
    )
