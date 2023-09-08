import os

# dynamically imports a class that corresponds to the file
# if a class is named foobar_model.py, it will import the class FooBar

folder = os.path.dirname(__file__)

for filename in os.listdir(folder):
    if not filename.endswith(".py") or filename.startswith("_") or "base" in filename:
        continue
    module, ext = os.path.splitext(filename)
    exec(f"from api.db.models.{module} import *")
