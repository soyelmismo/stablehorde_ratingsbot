import json
from pathlib import Path

class JsonDatabase:
    def __init__(self, filename="database.json"):
        self.file_path = Path(filename)

        # Carga los datos desde un archivo JSON al inicio
        self.load_data_from_json()

    def load_data_from_json(self):
        """
        Carga los datos del JSON.
        """
        try:
            with open(self.file_path, "r") as file:
                self.data = json.load(file)
        except ValueError:
            # Archivo vacío
            self.data = {}
        except FileNotFoundError:
            # El archivo no existe
            self.data = {}

    def save_data_to_json(self):
        """
        Guarda los datos en memoria a un archivo JSON.
        """
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)

    def user_exists(self, user_id, raise_exception: bool = False):
        if self.data.get(user_id):
            return True
        else:
            self.data[user_id] = {}

        if raise_exception:
            raise ValueError(f"User {user_id} doesn't exists...")
        return False

    def get(self, key):
        """
        Recupera un valor de los datos cargados.
        """
        return self.data.get(key)

    def set(self, key, value):
        """
        Actualiza el valor de la clave dada.
        """
        # Si la clave ya existe en la base de datos, actualiza solo las claves dadas 
        if key in self.data:
            self.data[key].update(value)
        # Si la clave no existe, crea un nuevo registro
        else:
            self.data[key] = value
        # Persiste los cambios en el archivo JSON
        self.save_data_to_json()

    def set_subkey(self, key, subkey, value):
        """
        Actualiza el valor de la subclave dada.
        """
        if key not in self.data:  # Si la clave no existe, crea un nuevo registro
            self.data[key] = {}
        self.data[key][subkey] = value  # Actualiza la subclave
        self.save_data_to_json()  # Persiste los cambios en el archivo JSON


    def delete(self, key):
        """
        Elimina un valor de los datos cargados.
        """
        if key in self.data:
            del self.data[key]
            self.save_data_to_json()  # Guarda los datos cada vez que eliminamos un valor

    def get_attributes_dict(self, user_id, keys: list):
        if not self.user_exists(user_id, raise_exception=True): return

        chat_dict = {key: self.data[user_id].get(key, None) for key in keys}

        return chat_dict
