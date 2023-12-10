#!/usr/bin/python3
"""
Defines the BaseModel class - Custom base class for the entire project.
"""

from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """
    Defines all common attributes/methods for the 
    other classes in the project.


    Arttributes:
        id (str): Handles unique user identity.
        created_at: Assigns current datetime.
        updated_at: Apdates current datetime.

    Methods:
        __str__: Prints the class name, id, and creates dictionary
        representations of the input values.
        save(self): Updates instance attrs with current datetime.
        to_dict(self): Returns the dict values of the instance obj.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel.
        Args:
            *args (tuples): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        date_time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                     self.__dict__[key] = datetime.strptime(value, date_time_format)
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value
                    
    def to_dict(self):
        """
        Return the dictionary of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        dict_objects = {}
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                dict_objects[key] = value.isoformat()
            else:
                dict_objects[key] = value
        dict_objects["__class__"] = self.__class__.__name__
        return dict_objects

    def save(self):
        """
        Update updated_at instance with the current datetime.
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def __str__(self):
        """
        Returns the print/str representation of the BaseModel.
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
