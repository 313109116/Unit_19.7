from typing import Union

import requests as r
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str):
        """Метод получения ключа API"""

        headers = {
            'email': email,
            'password': password
        }
        res = r.get(self.base_url + 'api/key', headers=headers)
        return PetFriends.__get_result(res)

    def get_pets(self, key: str, fltr: str = ''):
        """Метод получения списка собственных питомцев. fltr = 'my_pets'"""

        headers = {'auth_key': key}
        fltr = {'filter': fltr}

        res = r.get(self.base_url + 'api/pets', headers=headers, params=fltr)
        return PetFriends.__get_result(res)

    def add_pet(self, name: str, animal_type: str, age: str, key: str, pet_photo: str):
        """Метод добавления питомца на сайт"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'))
            })

        headers = {
            'auth_key': key,
            'Content-Type': data.content_type
        }

        res = r.post(self.base_url + 'api/pets', headers=headers, data=data)
        return PetFriends.__get_result(res)

    def update_pet(self, key: str, pet_id: str, name: str = '', animal_type: str = '', age: int = ''):
        """Метод изменения информации о питомце"""

        headers = {
            'auth_key': key
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = r.put(self.base_url + 'api/pets/{0}'.format(pet_id), headers=headers, data=data)
        return PetFriends.__get_result(res)

    def del_pet(self, key: str, pet_id: str):
        """Метод удаления питомца с сайта"""

        res = r.delete(self.base_url + 'api/pets/{0}'.format(pet_id), headers={'auth_key': key})
        return PetFriends.__get_result(res)

    @staticmethod
    def __get_result(res: r.models.Response) -> tuple[int, Union[str, dict]]:
        """Метод возврата результатов методов"""

        try:
            result = res.json()
        except:
            result = res.text
        return res.status_code, result