#!/usr/bin/env python3
"""Console module for the digital_cv project"""

import cmd
from app import create_app, db
from app.models import Store
from app.models import Strain
from app.models import User, Role

app = create_app()

# Create the database tables
with app.app_context():
    db.create_all()

class_dictionary = {
    'Strain': Strain,
    'Store': Store,
    'User': User,
    'Role': Role
}

class Strain_Console(cmd.Cmd):
    prompt = '(straingg_app) '

    def get_class(self, class_name):
        return class_dictionary.get(class_name)

    def do_create(self, arg):
        """Creates a new instance of a class: create <class> <attribute1=value1> <attribute2=value2> ..."""
        with app.app_context():
            params = arg.split()
            if len(params) < 1:
                print("Usage: create <class> <attribute1=value1> <attribute2=value2> ...")
                return

            class_name = params.pop(0)
            cls = self.get_class(class_name)
            if cls is None:
                print(f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            attributes = {}
            for param in params:
                key, value = param.split("=", 1)
                attributes[key] = value

        with app.app_context():
            if class_name == 'User' and 'role' in attributes:
                role_name = attributes.pop('role')
                password = attributes.pop('password', None)
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    print(f"Role {role_name} not found")
                    return
                instance = cls(**attributes)
                if password is not None:
                    instance.set_password(password)
                instance.roles.append(role)
            else:
                instance = cls(**attributes)

                db.session.add(instance)
                db.session.commit()
                print(f"{class_name} created with ID {instance.id}")

    def do_show(self, arg):
        """Show an instance of a class: show <class> <id>"""
        with app.app_context():
            params = arg.split()
            if len(params) < 2:
                print("Usage: show <class> <id>")
                return

            class_name, instance_id = params[0], params[1]
            cls = self.get_class(class_name)
            if cls is None:
                print(f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            instance = db.session.get(cls, instance_id)
            if instance is None:
                print(f"{class_name} with ID {instance_id} not found")
            else:
                print(instance)

    def do_destroy(self, arg):
        """Deletes an instance of a class: destroy <class> <id>"""
        with app.app_context():
            params = arg.split()
            if len(params) != 2:
                print("Usage: destroy <class> <id>")
                return

            class_name, instance_id = params
            cls = self.get_class(class_name)
            if cls is None:
                print(f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return
            
            instance = cls.query.get(instance_id)
            if instance is None:
                print(f"{class_name} with ID {instance_id} not found.")
                return

            db.session.delete(instance)
            db.session.commit()
            print(f"{class_name} with ID {instance_id} has been deleted.")

    def do_all(self, arg):
        """Displays all instances of a class: all <class>"""
        with app.app_context():
            params = arg.split()
            if len(params) != 1:
                print("Usage: all <class>")
                return

            class_name = params[0]
            cls = self.get_class(class_name)
            if cls is None:
                print(f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            instances = cls.query.all()
            for instance in instances:
                print(f"{class_name} {instance.id}: {instance}")

    def do_update(self, arg):
        """Updates an instance of a class: update <class> <id> <attribute1=value1> <attribute2=value2> ..."""
        with app.app_context():
            params = arg.split()
            if len(params) < 3:
                print("Usage: update <class> <id> <attribute1=value1> <attribute2=value2> ...")
                return

            class_name, instance_id = params[0], params[1]
            cls = self.get_class(class_name)
            if cls is None:
                print(f"Invalid class. Available classes: {', '.join(class_dictionary.keys())}")
                return

            instance = cls.query.get(instance_id)
            if instance is None:
                print(f"{class_name} with ID {instance_id} not found")
                return

            attributes = {}
            for param in params[2:]:
                key, value = param.split("=", 1)
                attributes[key] = value

            if class_name == 'User' and 'role' in attributes:
                role_name = attributes.pop('role')
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    print(f"Role {role_name} not found")
                    return

                user = instance
                user.roles.append(role)
                db.session.commit()
                print(f"Role {role_name} appended to User with ID {instance_id}")

            for key, value in attributes.items():
                setattr(instance, key, value)

            db.session.commit()
            print(f"{class_name} with ID {instance_id} has been updated.")

    def do_quit(self, arg):
        """Quit the console: quit"""
        print("Exiting console...")
        return True

if __name__ == "__main__":
    Strain_Console().cmdloop()
