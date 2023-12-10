#!/usr/bin/python3
"""
Defines the FileStorage class.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Custom class for file storage

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictionary __objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in a dict the obj with key.
        """
        obj_class_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_class_cname, obj.id)] = obj

    def save(self):
        """
        Serializes a dict to a JSON file.
        """
        objdict = FileStorage.__objects
        object_dict = {obj: objdict[obj].to_dict() for obj in objdict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(object_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to a dict
        """
        try:
            with open(FileStorage.__file_path) as f:
                object_dict = json.load(f)
                for o in object_dict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
