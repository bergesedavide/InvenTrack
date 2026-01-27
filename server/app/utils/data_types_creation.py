from app.config import DataTypes
import ast

class DataManipulation:
    def __init__(self):
        pass
    
    def literal_eval(self, value: str):
        return ast.literal_eval(value)

    def todict(self, key_list: list, value_list: list):

        type_map = {
            DataTypes.STRING.value: str,
            DataTypes.INTEGER.value: int,
            DataTypes.FLOAT.value: float,
            DataTypes.BOOLEAN.value: bool
        }

        new_key_list = []
        for k in key_list:
            if type(k) is type_map[DataTypes.BOOLEAN.value]:
                raise TypeError(f"{k} non può essere un bool")

            if type(k) is not type_map[DataTypes.STRING.value]:
                k = str(k)
                new_key_list.append(k)
            else:
                new_key_list.append(k)
            
        result_dict = dict(zip(new_key_list, value_list))
        return result_dict

    def tolist(self, **args):
        value_list = list(args)

        return value_list