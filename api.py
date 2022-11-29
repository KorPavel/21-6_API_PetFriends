# =============  Модуль 19  ===================
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Union


class PetFriends:
    """ API библиотека к веб-приложению Pet Friends """

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"


    def response_processing(self, resp):
        """ Обработка API ответов от сервера """
        status = resp.status_code
        content = resp.headers  # обязательно
        optional = resp.request.headers  # опционально
        result = ""
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        return status, result, content, optional


    def get_api_key(self, email: str, passwd: str) -> json:
        """ Метод делает запрос к API сервера и возвращает статус обработанного запроса и результат
         в формате JSON с уникальным ключом пользователя, найденного по указанным email и паролем """

        headers = {
            'email': email,
            'password': passwd,
        }
        res = requests.get(f'{self.base_url}api/key', headers=headers)
        return self.response_processing(res)


    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """ Метод делает запрос к API сервера и возвращает статус обработанного запроса и результат
        в формате JSON со списком найденных питомцев, совпадающих с фильтром. На данный момент
        фильтр может иметь либо пустое значение - получить список всех питомцев, либо 'my_pets' -
        получить список собственных питомцев """

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(f'{self.base_url}api/pets', headers=headers, params=filter)
        return self.response_processing(res)


    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: Union[int, float], pet_photo: str) -> json:
        """ Метод отправляет на сервер данные о добавляемом питомце и возвращает статус
        обработанного запроса на сервер и результат в формате JSON с данными добавленного питомца """

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(f'{self.base_url}api/pets', headers=headers, data=data)
        return self.response_processing(res)


    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """ Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус обработанного запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200 """

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(f'{self.base_url}api/pets/{pet_id}', headers=headers)
        return self.response_processing(res)


    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: Union[int, float]) -> json:
        """ Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
        возвращает статус обработанного запроса и result в формате JSON с обновлёнными данными питомца """

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(f'{self.base_url}api/pets/{pet_id}', headers=headers, data=data)
        return self.response_processing(res)


# ====================  Два API метода к заданию 19.7.2  =====================

    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str,
                           age: Union[int, float]) -> json:

        """ Метод отправляет на сервер данные без фото о добавляемом питомце и возвращает статус
        обработанного запроса с сервера и результат в формате JSON с данными добавленного питомца """

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(f'{self.base_url}api/create_pet_simple', headers=headers, data=data)
        return self.response_processing(res)


    def add_only_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:

        """ Метод отправляет на сервер фото существующего питомца и возвращает статус
        обработанного запроса с сервера и результат в формате JSON с данными питомца """

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(f'{self.base_url}api/pets/set_photo/{pet_id}', headers=headers, data=data)
        return self.response_processing(res)