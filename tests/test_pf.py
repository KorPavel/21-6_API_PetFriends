from api import PetFriends
from settings import *
import json
import os
import pytest


pf = PetFriends()

class TestIfValidAuthKey:
    def test_get_all_pets_with_valid_key(self, get_auth_key, filter=''):
        """ Проверяем, что запрос всех питомцев возвращает не пустой список.
        Запрашиваем список всех питомцев и проверяем, что список не пустой.
        Доступные значения параметра filter = 'my_pets' или ''. """

        status, result, content, optional = pf.get_list_of_pets(get_auth_key, filter)
        with open('out_json.json', 'w', encoding='utf8') as write:
            json.dump(result, write, ensure_ascii=False, indent=4)

        assert status == 200
        assert len(result['pets']) > 0
        print(f'\nContent: {content}\n\nOptional: {optional}')


    def test_get_a_list_of_the_user_pets_with_a_valid_key(self, get_auth_key, filter='my_pets'):
        """ Проверяем, что запрос питомцев пользователя проходит со статусом 200 и возвращает список
        его питомцев. Добавляем пользователю одного питомца в случае, если список пуст. """

        # Запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пустой, то добавляем нового и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        status, my_pets, content, optional = pf.get_list_of_pets(get_auth_key, filter)
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(my_pets['pets']) > 0
        print(f'\nContent: {content}\n\nOptional: {optional}')  # получаем заголовки в Terminal


    def test_create_pet_simple_with_valid_data(self, get_auth_key, name='Крош',
                                               animal_type='кролик', age='5'):
        """  Проверяем, что можно добавить питомца с корректными данными без фотографии """

        # Добавляем питомца без фотографии
        status, result, content, optional = pf.add_new_pet_simple(get_auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        print(f'\nContent: {content}\n\nOptional: {optional}')


    @pytest.mark.add_file
    def test_successful_add_photo_jpg_of_pet(self, get_auth_key, pet_photo='images/losyash-12.jpg'):
        """Проверяем, что можно добавить фото питомца в формате .jpg"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo).replace('\\', '/')

        # Запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Берём id первого питомца из списка и отправляем запрос на добавление фото
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.add_only_photo_of_pet(get_auth_key, pet_id, pet_photo)
        with open('out_json.json', 'w', encoding='utf8') as write:
            json.dump(result, write, ensure_ascii=False, indent=4)

        assert status == 200
        assert 'image/jpeg' in result['pet_photo']
        print(f'\nContent: {content}\n\nOptional: {optional}')


    @pytest.mark.add_file
    def test_successful_add_photo_png_of_pet(self, get_auth_key, pet_photo='images/krosh-3.png'):
        """Проверяем, что можно добавить фото питомца в формате .png"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo).replace('\\', '/')

        # Запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Крош', 'кролик', '5')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Берём id первого питомца из списка и отправляем запрос на добавление фото
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.add_only_photo_of_pet(get_auth_key, pet_id, pet_photo)
        with open('out_json.json', 'w', encoding='utf8') as write:
            json.dump(result, write, ensure_ascii=False, indent=4)

        assert status == 200
        assert 'image/jpeg' in result['pet_photo']
        print(f'\nContent: {content}\n\nOptional: {optional}')


    @pytest.mark.add_file
    def test_add_new_pet_with_valid_data(self, get_auth_key, name='Крош', animal_type='кролик',
                                         age='5', pet_photo='images/krosh-8.jpg'):
        """ Проверяем, что можно добавить питомца с фото и с корректными данными """

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo).replace('\\', '/')

        # Добавляем питомца
        status, result, content, optional = pf.add_new_pet(get_auth_key, name, animal_type, age, pet_photo)
        with open('out_json.json', 'w', encoding='utf8') as write:
            json.dump(result, write, ensure_ascii=False, indent=4)  # Получаем тело ответа в файл

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        print(f'\nContent: {content}\n\nOptional: {optional}')


    def test_successful_update_self_pet_info(self, get_auth_key, name='Крош', animal_type='кролик', age='5'):
        """Проверяем возможность обновления информации о питомце"""

        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Берём id первого питомца из списка и отправляем запрос на обновление информации
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.update_pet_info(get_auth_key,
                                                               pet_id, name, animal_type, age)
        with open('out_json.json', 'w', encoding='utf8') as write:
            json.dump(result, write, ensure_ascii=False, indent=4)  # Получаем тело ответа в файл

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        print(f'\nContent: {content}\n\nOptional: {optional}')


    def test_successful_update_self_pet_name(self, get_auth_key, name='Krosh', animal_type='', age=''):
        ''' Проверяем, что можно корректно изменить только имя питомца,
        остальные данные остались прежними '''

        # Запрашиваем список СВОИХ питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        pet_id = my_pets['pets'][0]['id']
        pet_type = my_pets['pets'][0]['animal_type']
        pet_age = my_pets['pets'][0]['age']
        status, result, content, optional = pf.update_pet_info(get_auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200, изменилось только имя, остальные данные остались прежними
        assert status == 200
        assert result['name'] == name
        assert result['id'] == pet_id
        assert result['animal_type'] == pet_type
        assert result['age'] == pet_age
        print(f'\nContent: {content}\n\nOptional: {optional}')


    def test_successful_update_self_pet_animal_type(self, get_auth_key, name='', animal_type='барсук', age=''):
        ''' Проверяем, что можно корректно изменить только тип питомца,
        остальные данные остались прежними '''

        # Запрашиваем список СВОИХ питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')
        pet_id = my_pets['pets'][0]['id']
        pet_name = my_pets['pets'][0]['name']
        pet_age = my_pets['pets'][0]['age']
        status, result, content, optional = pf.update_pet_info(get_auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200, изменился только тип, остальные данные остались прежними
        assert status == 200
        assert result['animal_type'] == animal_type
        assert result['id'] == pet_id
        assert result['name'] == pet_name
        assert result['age'] == pet_age
        print(f'\nContent: {content}\n\nOptional: {optional}')


    def test_successful_update_self_pet_age(self, get_auth_key, name='', animal_type='', age='1.3'):
        ''' Проверяем, что можно корректно изменить только возраст питомца,
        остальные данные остались прежними '''

        # Запрашиваем список СВОИХ питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')
        pet_id = my_pets['pets'][0]['id']
        pet_name = my_pets['pets'][0]['name']
        pet_type = my_pets['pets'][0]['animal_type']

        status, result, content, optional = pf.update_pet_info(get_auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 200, изменился только возраст, остальные данные остались прежними
        assert status == 200
        assert result['age'] == str(age)
        assert result['id'] == pet_id
        assert result['animal_type'] == pet_type
        assert result['name'] == pet_name
        print(f'\nContent: {content}\n\nOptional: {optional}')


    def test_successful_delete_self_pet(self, get_auth_key):
        """ Проверяем возможность удаления питомца """

        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пустой, то добавляем нового и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        with open('out_json.json', 'w', encoding='utf8') as write:
            json.dump(my_pets, write, ensure_ascii=False, indent=4)

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.delete_pet(get_auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()
        print(f'\nContent: {content}\n\nOptional: {optional}')


    def test_correct_keys_from_get_all_pets(self, get_auth_key, filter=''):
        """ Проверка, что в ответе приходят корректные ключи,
        соответствующие спецификации при запросе списка питомцев"""
        sample = {"age": int,
                  "animal_type": str,
                  "created_at": str,
                  "id": str,
                  "name": str,
                  "pet_photo": str
                  }
        # получаем список всех питомцев из базы, далее выбираем первого
        _, result, _, _ = pf.get_list_of_pets(get_auth_key, filter)

        # сравниваем ключи из ответа с образцом из спецификации
        assert result['pets'][0].keys() == sample.keys()


    @pytest.mark.xfail
    def test_correct_values_from_get_all_pets(self, get_auth_key, filter=''):
        """ Проверка, что в ответе приходят корректные типы значений параметров,
        соответствующие спецификации при запросе списка питомцев
       Тест падает, т.к. тип age не соответствует спецификации (д.б. int) """
        sample = {"age": int,
                  "animal_type": str,
                  "created_at": str,
                  "id": str,
                  "name": str,
                  "pet_photo": str
                  }
        # получаем список всех питомцев из базы, далее выбираем первого
        _, result, _, _ = pf.get_list_of_pets(get_auth_key, filter)

        # сравниваем типы значений параметров из ответа с образцом из спецификации
        for actual, expected in zip(result['pets'][0].values(), sample.values()):
            assert type(actual) == expected


    # ~~~~~~~~~~  Негативные тесты  ~~~~~~~~~~~
    @pytest.mark.negative
    def test_dont_get_list_of_pets_with_incorrect_filter(self, request, get_auth_key, filter='pets'):
        """Метод проверяет, что в параметр фильтр нельзя ввести неподдерживаемое значение,
        запрос к серверу выдает внутреннюю ошибку на стороне сервера"""

        status, result, content, optional = pf.get_list_of_pets(get_auth_key, filter)
        with open('errors_file.txt', 'a', encoding='utf8') as f:
            f.write(f"{request.node.name}\n{self.test_dont_get_list_of_pets_with_incorrect_filter.__doc__}\n{result}\n")

        assert status == 500
        print(f'\nContent: {content}\n\nOptional: {optional}')


    @pytest.mark.negative
    @pytest.mark.add_file
    @pytest.mark.xfail
    def test_add_text_file_instead_of_a_photo(self, get_auth_key, request, name='Krosh',
                                              animal_type='rabbit', age='5',
                                              pet_photo='images/wrong_photo.txt'):
        """ Проверяем, что при создании нового питомца нельзя добавить
        текстовый файл вместо фото """
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo).replace('\\', '/')

        # Добавляем питомца
        status, result, content, optional = pf.add_new_pet(get_auth_key, name, animal_type, age, pet_photo)
        with open('errors_file.txt', 'a', encoding='utf8') as f:
            f.write(f"\n{request.node.name}\n{self.test_add_text_file_instead_of_a_photo.__doc__}\n{result}\n")

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
        assert result['pet_photo'] == ''
        print(f'\nContent: {content}\n\nOptional: {optional}')


    @pytest.mark.negative
    @pytest.mark.add_file
    @pytest.mark.xfail
    def test_add_audio_file_instead_of_a_photo(self, get_auth_key, request, name='Krosh',
                                               animal_type='rabbit', age='5',
                                               pet_photo='images/Fine.mp3'):
        """ Проверяем, что при создании нового питомца нельзя добавить
        аудио файл вместо фото """
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo).replace('\\', '/')

        # Добавляем питомца
        status, result, content, optional = pf.add_new_pet(get_auth_key, name, animal_type, age, pet_photo)
        with open('errors_file.txt', 'a', encoding='utf8') as f:
            f.write(f"\n{request.node.name}\n{self.test_add_audio_file_instead_of_a_photo.__doc__}\n{result}\n")

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
        assert result['pet_photo'] == ''
        print(f'\nContent: {content}\n\nOptional: {optional}')


    @pytest.mark.negative
    @pytest.mark.add_file
    def test_failed_text_file(self, get_auth_key, request, pet_photo='images/wrong_photo.txt'):
        """ Проверяем, что при обновлении фото питомца нельзя прикрепить текстовый файл вместо фото """

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo).replace('\\', '/')

        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Стрелка', 'белка', '10')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Берём id первого питомца из списка и отправляем запрос на обновление информации
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.add_only_photo_of_pet(get_auth_key,
                                                                     pet_id, pet_photo)
        with open('errors_file.txt', 'a', encoding='utf8') as f:
            f.write(f"\n{request.node.name}\n{self.test_failed_text_file.__doc__}\n{result}\n")  # Получаем тело ответа в файл

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 500
        print(f'\nContent: {content}\n\nOptional: {optional}')


    @pytest.mark.negative
    @pytest.mark.add_file
    def test_failed_audio_file(self, get_auth_key, request, pet_photo='images/Fine.mp3'):
        """ Проверяем, что при обновлении фото питомца нельзя прикрепить аудио файл вместо фото """

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo).replace('\\', '/')

        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пуст, то добавляем нового без фото и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Стрелка', 'белка', '10')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Берём id первого питомца из списка и отправляем запрос на обновление информации
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.add_only_photo_of_pet(get_auth_key,
                                                                     pet_id, pet_photo)
        with open('errors_file.txt', 'a', encoding='utf8') as f:
            f.write(f"\n{request.node.name}\n{self.test_failed_audio_file.__doc__}\n{result}\n")  # Получаем тело ответа в файл

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 500
        # assert result['name'] == name
        print(f'\nContent: {content}\n\nOptional: {optional}')


@pytest.mark.negative
def test_get_api_key_for_invalid_password(request, email=valid_email, password=invalid_password):
    ''' Проверяем, что при вводе неправильного пароля нельзя получить API ключ '''

    # Отправляем запрос, ожидаем ошибку
    status, result, content, optional = pf.get_api_key(email, password)
    with open('errors_file.txt', 'a', encoding='utf8') as f:
        f.write(f"\n{request.node.name}\n{test_get_api_key_for_invalid_password.__doc__}\n{result}\n")
    assert status == 403
    print(f'\nContent: {content}\n\nOptional: {optional}')


@pytest.mark.negative
def test_get_api_key_for_invalid_email(request, email=invalid_email, password=valid_password):
    ''' Проверяем, что при вводе неправильного e-mail нельзя получить API ключ '''

    # Отправляем запрос, ожидаем ошибку
    status, result, content, optional = pf.get_api_key(email, password)
    with open('errors_file.txt', 'a', encoding='utf8') as f:
        f.write(f"\n{request.node.name}\n{test_get_api_key_for_invalid_email.__doc__}\n{result}\n")
    assert status == 403
    print(f'\nContent: {content}\n\nOptional: {optional}')


@pytest.mark.negative
def test_get_my_pet_info_with_wrong_key(request, filter='my_pets'):
    ''' Проверяем невозможность получения информации о питомцах, если указан неверный ключ '''
    # Отправляем запрос, ожидаем ошибку
    auth_key = {'key': '123'}
    status, result, content, optional = pf.get_list_of_pets(auth_key, filter)
    with open('errors_file.txt', 'a', encoding='utf8') as f:
        f.write(f"\n{request.node.name}\n{test_get_my_pet_info_with_wrong_key.__doc__}\n{result}\n")
    assert status == 403
    print(f'\nContent: {content}\n\nOptional: {optional}')