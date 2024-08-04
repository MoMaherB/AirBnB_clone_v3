#!/usr/bin/python3
"""FileStorage Class"""
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
import json
import shlex


class FileStorage():
    """FileStorage class that serializes instances to
    a JSON file and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    my_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State
    }

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace('.', ' ')
                partition = shlex.split(partition)
                if (partition[0] == cls.__name__):
                    dic[key] = self.__objects[key]
            return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """sets obj to objects dict"""
        obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[obj_key] = obj

    def save(self):
        """That method serializes __objects to
        the JSON file (path: __file_path)"""

        jason_objects = {}
        for id, object in FileStorage.__objects.items():
            jason_objects[id] = object.to_dict()

        with open(FileStorage.__file_path, "w") as file:
            json.dump(jason_objects, file)

    def reload(self):
        """ deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists"""

        try:
            with open(FileStorage.__file_path, "r") as file:
                json_objects = json.load(file)

                for dict_object in json_objects.values():
                    # Retrieve the class from my_classes
                    MyClass = dict_object["__class__"]
                    MyClassName = FileStorage.my_classes.get(MyClass)
                    if MyClassName:
                        self.new(MyClassName(**dict_object))

        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete an existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]
