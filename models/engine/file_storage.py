#!/usr/bin/python3
"""This module defines a class to manage File storage for hbnb clone"""

import json
from models.base_model import BaseModel

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, "w", encoding="utf-8") as file:
            obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                obj_dict = json.load(file)
                for key, obj_attr in obj_dict.items():
                    cls_name, obj_id = key.split(".")
                    cls = BaseModel.__subclasses__()[0]
                    if cls_name in globals():
                        cls = globals()[cls_name]
                    obj = cls(**obj_attr)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from __objects if it exists"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
            self.save()

    def close(self):
        """Calls reload method for deserialization"""
        self.reload()

