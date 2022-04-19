import json

validators = {}
def getValidator(collection_name: str):
    """Obtain a validator data of a collection which is stored as a json file with the same name

    parameters:
        collection_name -- the name of the collection, which should also be the filename

    returns:
        validator -- dict in the format of a mongo collection validator
    """
    if collection_name not in validators:
        with open(f'./src/static/validators/{collection_name}.json', 'r') as f:
            validators[collection_name] = json.load(f)
    return validators[collection_name]