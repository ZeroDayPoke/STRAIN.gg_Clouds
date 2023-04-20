#!/usr/bin/env python3
import cmd
from models import storage
from models.user import User
from models.strain import Strain

class StrainConsole(cmd.Cmd):
    prompt = '(STRAIN.gg) '

    def do_create(self, arg):
        """Creates a new instance of a class: create <class> <attribute1=value1> <attribute2=value2> ..."""
        params = arg.split()
        if len(params) < 1:
            print("Usage: create <class> <attribute1=value1> <attribute2=value2> ...")
            return

        class_name = params.pop(0)
        if class_name not in storage.class_dictionary:
            print(f"Invalid class. Available classes: {', '.join(storage.class_dictionary.keys())}")
            return

        attributes = {}
        for param in params:
            key, value = param.split("=", 1)
            attributes[key] = value

        instance = storage.class_dictionary[class_name](**attributes)
        storage.new(instance)
        storage.save()
        print(f"{class_name} created with ID {instance.id}")

    def do_all(self, arg):
        """Return all instances of a given model class or all instances of all model classes."""
        if arg:
            if arg not in storage.class_dictionary:
                print(f"Invalid class name. Supported classes: {', '.join(storage.class_dictionary.keys())}")
                return
            objects = storage.all(arg)
            for obj in objects:
                print(obj)
        else:
            for cls in storage.class_dictionary.values():
                objects = storage.all(cls)
                for obj in objects:
                    print(obj)

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id: show <class> <id>"""
        params = arg.split()
        if len(params) != 2:
            print("Usage: show <class> <id>")
            return

        class_name, obj_id = params
        instance = storage.get(class_name, obj_id)
        if instance is None:
            print("Instance not found.")
        else:
            print(instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id: destroy <class> <id>"""
        params = arg.split()
        if len(params) != 2:
            print("Usage: destroy <class> <id>")
            return

        class_name, obj_id = params
        instance = storage.get(class_name, obj_id)
        if instance is None:
            print("Instance not found.")
        else:
            storage.delete(instance)
            storage.save()
            print(f"Instance of {class_name} with ID {obj_id} deleted.")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value: update <class> <id> <attribute> <value>"""
        params = arg.split()
        if len(params) != 4:
            print("Usage: update <class> <id> <attribute> <value>")
            return

        class_name, obj_id, attribute, value = params
        instance = storage.get(class_name, obj_id)
        if instance is None:
            print("Instance not found.")
        else:
            if hasattr(instance, attribute):
                setattr(instance, attribute, value)
                storage.save()
                print(f"Instance of {class_name} with ID {obj_id} updated.")
            else:
                print(f"Attribute '{attribute}' not found in {class_name}.")

    def do_quit(self, arg):
        """Quit the console: quit"""
        print("Exiting console...")
        storage.close()
        return True

if __name__ == "__main__":
    StrainConsole().cmdloop()
