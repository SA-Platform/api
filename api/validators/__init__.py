import os

# dynamically imports all classes in python files

folder = os.path.dirname(__file__)

for filename in os.listdir(folder):
    if not filename.endswith(".py") or filename.startswith("_"):
        continue
    module, ext = os.path.splitext(filename)

    exec(f"from api.validators.{module} import *")
