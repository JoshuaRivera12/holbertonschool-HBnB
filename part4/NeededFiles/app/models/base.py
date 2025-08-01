from app.db import db

class Base:
    def to_dict(self):
        """Returns a dictionary containing all key-value pairs of the object."""
        new_dict = self.__dict__.copy()
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict
