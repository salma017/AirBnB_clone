#!/usr/bin/python3
"""
The console v: 01
The entry point of the command interpreter
"""

import cmd
import json
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split
from models.__init__ import storage

class HBNBCommand(cmd.Cmd):
    """
    Defines the HBNB command interepter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def precmd(self, line):
        """
        Defines instructions to execute before <line> is interpreted."""        
        if not line:
            return '\n'

        pattern = re.compile(r"(\w+)\.(\w+)\((.*)\)")
        match_list = pattern.findall(line)
        if not match_list:
            return super().precmd(line)

        match_tuple = match_list[0]
        if not match_tuple[2]:
            if match_tuple[1] == "count":
                instance_objs = storage.all()
                print(len([
                    v for _, v in instance_objs.items()
                    if type(v).__name__ == match_tuple[0]]))
                return "\n"
            return "{} {}".format(match_tuple[1], match_tuple[0])
        else:
            args = match_tuple[2].split(", ")
            if len(args) == 1:
                return "{} {} {}".format(
                    match_tuple[1], match_tuple[0],
                    re.sub("[\"\']", "", match_tuple[2]))
            else:
                match_json = re.findall(r"{.*}", match_tuple[2])
                if (match_json):
                    return "{} {} {} {}".format(
                        match_tuple[1], match_tuple[0],
                        re.sub("[\"\']", "", args[0]),
                        re.sub("\'", "\"", match_json[0]))
                return "{} {} {} {} {}".format(
                    match_tuple[1], match_tuple[0],
                    re.sub("[\"\']", "", args[0]),
                    re.sub("[\"\']", "", args[1]), args[2])

    def emptyline(self):
        """Eliminates empty lines."""
        pass

    def valid_classname(args, check_id=False):
        """Runs checks on args to validate classname entry."""
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in current_classes.keys():
            print("** class doesn't exist **")
            return False
        if len(args) < 2 and check_id:
            print("** instance id missing **")
            return False
        return True

    def valid_attrs(args):
        """
        Checks on args to validate classname attributes and values."""
        if len(args) < 3:
            print("** attribute name missing **")
            return False
        if len(args) < 4:
            print("** value missing **")
            return False
        return True

    def is_float(x):
        """Checks if x is float."""
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True
    
    def is_int(x):
        """Checks if x is an integer."""
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b
    
    def parsed_str(arg):
        """Parse `arg` to an `int`, `float` or `string`."""
        parsed = re.sub("\"", "", arg)

        if is_int(parsed):
            return int(parsed)
        elif is_float(parsed):
            return float(parsed)
        else:
            return arg

    def do_quit(self, arg):
        """Quits command to exit program."""
        return True

    def do_EOF(self, arg):
        """
        Quits command interpreter with ctrl+d.
        Args:
            arg: inout argument to quit termina.
        """
        return True

    def do_create(self, arg):
        """Create a new instance.
        Args:
            arg (str): Command passed into the interpreter.
        """
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.__module_names:
            print("** class doesn't exist **")
        else:
            args = arg.split()
            class_name = args[0]
            new_class = globals()[class_name]()
            new_class.save()
            print(new_class.id)
 
    def do_show(self, arg):
        """
        Displays the string representation of a class instance."""

        args = arg.split()
        if not validate_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return
        print(req_instance)
 
    def do_destroy(self, arg):
        """Delete a class instance of a given id."""

        args = arg.split()
        if not valid_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return

        del instance_objs[key]
        storage.save()
 
    def do_all(self, arg):
        """Displays all the instances with the attributes.
        Args:
            arg (str): Command passed into the interpreter.
        """
        args = arg.split()
        all_obj = storage.all()
        obj_list = []

        if not args:
            for obj in all_obj.values():
                obj_list.append(str(obj))
            print(obj_list)
        elif args[0] not in HBNBCommand.__module_names:
            print("** class doesn't exist **")
        else:
            for key, obj in all_obj.items():
                class_name, obj_id = key.split(".")
                if class_name == args[0]:
                    obj_list.append(str(obj))
                print(obj_list)
 
    def do_update(self, arg):
        """Updates an instance based on the class name and id."""

        args = arg.split(maxsplit=3)
        if not valid_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return

        match_json = re.findall(r"{.*}", arg)
        if match_json:
            payload = None
            try:
                payload: dict = json.loads(match_json[0])
            except Exception:
                print("** invalid syntax **")
                return
            for key, value in payload.items():
                setattr(req_instance, key, value)
            storage.save()
            return
        if not valid_attrs(args):
            return
        first_attr = re.findall(r"^[\"\'](.*?)[\"\']", args[3])
        if first_attr:
            setattr(req_instance, args[2], first_attr[0])
        else:
            value_list = args[3].split()
            setattr(req_instance, args[2], parsed_str(value_list[0]))
        storage.save()

    def do_count(self, arg):
        """Retrieves the number of instances of a given class."""

        count = 0
        for instance_object in storage.all().values():
            if instance_object.__class__.__name__ == arg:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
