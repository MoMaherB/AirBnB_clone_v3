#!/usr/bin/python3
"""BaseModel Class"""
import models
from datetime import datetime
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseModel():
    """Base Model class parent for all classes"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """Initialization of BaseModel object"""
        if kwargs:
            if "__class__" in kwargs:
                del kwargs["__class__"]
            for key, value in kwargs.items():
                if key in ["updated_at", "created_at"]:
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """The custom representation for printing BaseModel object"""

        class_name = self.__class__.__name__
        what_a_dict = self.__dict__.copy()
        if '_sa_instance_state' in what_a_dict:
            del what_a_dict['_sa_instance_state']
        return "[{}] ({}) {}".format(class_name, self.id, what_a_dict)

    def save(self):
        """to update time after each new save of an object"""

        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__ of the
        instance with class name as a value and key __class__"""

        my_dict = {'__class__': self.__class__.__name__}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if key == "updated_at" or key == "created_at":
                    my_dict[key] = value.isoformat()
                else:
                    my_dict[key] = value
        return my_dict

    def delete(self):
        """ delete object
        """
        models.storage.delete(self)
