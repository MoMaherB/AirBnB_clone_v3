#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey


class Review(BaseModel, Base):
    """
    class Review that inherits from BaseModel:
    place_id (str): The Place id.
    user_id (str): The User id.
    text (str): The text of the review.
    """

    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
