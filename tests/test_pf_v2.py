from api import PetFriends
from settings import *
import os
import pytest
import time


pf = PetFriends()

def generate_string(num):
   return "x" * num

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

str_params = ['', generate_string(255), generate_string(1001), russian_chars(),
              russian_chars().upper(), chinese_chars(), special_chars(), 123]
str_names = ['empty string', '255 symbols', 'more than 1000 symbols', 'russian',
             'RUSSIAN', 'chinese', 'specials', 'digit']
age_params = ['', '-1', '0', '1', '100', '1.5', '2147483647', '2147483648',
              special_chars(), russian_chars(), russian_chars().upper(),
              chinese_chars()]
age_names = ['empty string', 'negative', 'zero', 'min', 'greater than max', 'float',
             'int_max', 'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese']

def is_age_valid(age):
    # Проверяем, что возраст - это число от 1 до 49 и целое
    return age.isdigit() and 0 < int(age) < 50 and float(age) == int(age)


def log_request(*args, **kwargs):
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    ex_time = kwargs.values()
    t_name, _, t_doc = args[0].partition('\n')
    head = f"\n{'░' * 12}\n░ {datetime.now().strftime('%H:%M:%S')} ░\t" \
           f"{t_name.replace('_', ' ').capitalize()}\n{'░' * 12}\n{t_doc}\n"
    with open(os.path.join(log_path, log_file), 'a', encoding='utf-8') as f:
        f.write(head)
        f.write(f'Время выполнения теста {int(*ex_time)/1000} сек.\n')
        for el in args[1:]:
            if 'Access-Control-Allow-Origin' in el:
                f.write(f'Content: {str(el)}\n')
            elif 'User-Agent' in el:
                f.write(f'Optional: {str(el)}\nBody: ')
            else:
                f.write(f'{str(el)[:255]} ...\n' if len(str(el)) > 255 else f'{str(el)}\n')


class TestIfValidAuthKey:

    @pytest.mark.parametrize('filter', ['', 'my_pets'], ids=['empty string', 'only my pets'])
    def test_get_a_list_of_the_user_pets_with_a_valid_filter(self, request, get_auth_key, filter):
        """ Проверяем, что запрос питомцев на получение информации о питомцах успешно проходит
        при валидных значениях параметра 'фильтр'. Доступные значения параметра filter = 'my_pets' или ''."""

        start_time = time.time_ns()  # запускаем таймер
        # Запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пустой, то добавляем нового и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        status, my_pets, content, optional = pf.get_list_of_pets(get_auth_key, filter)
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(my_pets['pets']) > 0
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_get_a_list_of_the_user_pets_with_a_valid_filter.__doc__}\n'
        log_request(title, content, optional, my_pets, rt=res_time)


    @pytest.mark.parametrize('name', str_params[1: -1]+['123'], ids=str_names[1:])
    @pytest.mark.parametrize('animal_type', str_params[1: -1] + ['123'], ids=str_names[1:])
    @pytest.mark.parametrize('age', ['1'], ids=['min'])
    def test_create_pet_simple_with_valid_data(self, request, get_auth_key, name, animal_type, age):
        """  Проверяем, что можно добавить питомца с корректными данными без фотографии """

        start_time = time.time_ns()  # запускаем таймер
        # Добавляем питомца без фотографии
        status, result, content, optional = pf.add_new_pet_simple(get_auth_key, name, animal_type, age)
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Сверяем полученный ответ с ожидаемым результатом
        # if name == '' or animal_type == '' or is_age_valid(age):
        #     assert status == 400
        # else:
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_create_pet_simple_with_valid_data.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    @pytest.mark.xfail
    @pytest.mark.parametrize('name', [''], ids=['empty string'])
    @pytest.mark.parametrize('animal_type', [''], ids=['empty string'])
    @pytest.mark.parametrize('age', age_params, ids=age_names)
    def test_create_pet_simple_negative(self, request, get_auth_key, name, animal_type, age):
        """  Проверяем, что можно добавить питомца без имени и/или без типа животного и/или
        с некорректным возрастом без фотографии """

        start_time = time.time_ns()  # запускаем таймер
        # Добавляем питомца без фотографии
        status, result, content, optional = pf.add_new_pet_simple(get_auth_key, name, animal_type, age)
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_create_pet_simple_negative.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    @pytest.mark.add_file
    @pytest.mark.parametrize('pet_file', ['losyash-12.jpg', 'krosh-3.png'], ids=['format (.jpg)', 'format (.png)'])
    def test_successful_add_photo_jpg_of_pet(self, request, get_auth_key, pet_file):
        """Проверяем, что можно добавить фото питомца в форматах .jpg и .png """

        start_time = time.time_ns()  # запускаем таймер
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), f'images/{pet_file}').replace('\\', '/')

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
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        assert status == 200
        assert 'image/jpeg' in result['pet_photo']
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_successful_add_photo_jpg_of_pet.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    @pytest.mark.add_file
    @pytest.mark.parametrize('name', str_params[1: -1] + ['123'], ids=str_names[1:])
    @pytest.mark.parametrize('animal_type', str_params[1: -1] + ['123'], ids=str_names[1:])
    @pytest.mark.parametrize('age', ['1'], ids=['min'])
    @pytest.mark.parametrize('pet_file', ['losyash-12.jpg', 'krosh-3.png'], ids=['format (.jpg)', 'format (.png)'])
    def test_add_new_pet_with_valid_data(self, request, get_auth_key, name, animal_type, age, pet_file):
        """ Проверяем, что можно добавить питомца с фото и с корректными данными """

        start_time = time.time_ns()  # запускаем таймер
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), f'images/{pet_file}').replace('\\', '/')

        # Добавляем питомца
        status, result, content, optional = pf.add_new_pet(get_auth_key, name, animal_type, age, pet_photo)
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_add_new_pet_with_valid_data.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    @pytest.mark.parametrize('name', str_params[1: -1] + ['123'], ids=str_names[1:])
    @pytest.mark.parametrize('animal_type', str_params[1: -1] + ['123'], ids=str_names[1:])
    @pytest.mark.parametrize('age', ['1'], ids=['min'])
    def test_successful_update_self_pet_info(self, request, get_auth_key, name, animal_type, age):
        """Проверяем возможность обновления информации о питомце"""

        start_time = time.time_ns()  # запускаем таймер
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
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_successful_update_self_pet_info.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)

    @pytest.mark.parametrize('name', str_params[1: -1] + ['123'], ids=str_names[1:])
    def test_successful_update_self_pet_name(self, request, get_auth_key, name, animal_type='', age=''):
        ''' Проверяем, что можно корректно изменить только имя питомца,
        остальные данные остались прежними '''

        start_time = time.time_ns()  # запускаем таймер
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
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Проверяем что статус ответа = 200, изменилось только имя, остальные данные остались прежними
        assert status == 200
        assert result['name'] == name
        assert result['id'] == pet_id
        assert result['animal_type'] == pet_type
        assert result['age'] == pet_age
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_successful_update_self_pet_name.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)

    @pytest.mark.parametrize('animal_type', str_params[1: -1] + ['123'], ids=str_names[1:])
    def test_successful_update_self_pet_animal_type(self, request, get_auth_key, animal_type, name='', age=''):
        ''' Проверяем, что можно корректно изменить только тип питомца,
        остальные данные остались прежними '''

        start_time = time.time_ns()  # запускаем таймер
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
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Проверяем что статус ответа = 200, изменился только тип, остальные данные остались прежними
        assert status == 200
        assert result['animal_type'] == animal_type
        assert result['id'] == pet_id
        assert result['name'] == pet_name
        assert result['age'] == pet_age
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_successful_update_self_pet_animal_type.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    def test_successful_update_self_pet_age(self, request, get_auth_key, name='', animal_type='', age='1.3'):
        ''' Проверяем, что можно корректно изменить только возраст питомца,
        остальные данные остались прежними '''

        start_time = time.time_ns()  # запускаем таймер
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
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Проверяем что статус ответа = 200, изменился только возраст, остальные данные остались прежними
        assert status == 200
        assert result['age'] == str(age)
        assert result['id'] == pet_id
        assert result['animal_type'] == pet_type
        assert result['name'] == pet_name
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_successful_update_self_pet_age.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    def test_successful_delete_self_pet(self, request, get_auth_key):
        """ Проверяем возможность удаления питомца """

        start_time = time.time_ns()  # запускаем таймер
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Проверяем - если список своих питомцев пустой, то добавляем нового и
        # повторно запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet_simple(get_auth_key, 'Лосяш', 'лось', '6')
            _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, result, content, optional = pf.delete_pet(get_auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, "my_pets")
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_successful_delete_self_pet.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    def test_correct_keys_from_get_all_pets(self, request, get_auth_key, filter=''):
        """ Проверка, что в ответе приходят корректные ключи,
        соответствующие спецификации при запросе списка питомцев"""
        sample = {"age": int,
                  "animal_type": str,
                  "created_at": str,
                  "id": str,
                  "name": str,
                  "pet_photo": str
                  }
        start_time = time.time_ns()  # запускаем таймер
        # получаем список всех питомцев из базы, далее выбираем первого
        _, result, content, optional = pf.get_list_of_pets(get_auth_key, filter)
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # сравниваем ключи из ответа с образцом из спецификации
        assert result['pets'][0].keys() == sample.keys()
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_correct_keys_from_get_all_pets.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    @pytest.mark.xfail
    def test_correct_values_from_get_all_pets(self, request, get_auth_key, filter=''):
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
        start_time = time.time_ns()  # запускаем таймер
        # получаем список всех питомцев из базы, далее выбираем первого
        _, result, content, optional = pf.get_list_of_pets(get_auth_key, filter)
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # сравниваем типы значений параметров из ответа с образцом из спецификации
        for actual, expected in zip(result['pets'][0].values(), sample.values()):
            assert type(actual) == expected
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_correct_values_from_get_all_pets.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    # ~~~~~~~~~~  Негативные тесты  ~~~~~~~~~~~
    @pytest.mark.negative
    @pytest.mark.parametrize('filter', str_params[1:], ids=str_names[1:])
    def test_dont_get_list_of_pets_with_incorrect_filter(self, request, get_auth_key, filter):
        """Метод проверяет, что в параметр фильтр нельзя ввести неподдерживаемое значение,
        запрос к серверу выдает внутреннюю ошибку на стороне сервера"""

        start_time = time.time_ns()  # запускаем таймер
        status, result, content, optional = pf.get_list_of_pets(get_auth_key, filter)
        with open('errors_file.txt', 'a', encoding='utf8') as f:
            f.write(f"{request.node.name}\n{self.test_dont_get_list_of_pets_with_incorrect_filter.__doc__}\n{result}\n")
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        assert status == 500
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_dont_get_list_of_pets_with_incorrect_filter.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    @pytest.mark.negative
    @pytest.mark.add_file
    @pytest.mark.xfail
    @pytest.mark.parametrize('pet_file', ['wrong_photo.txt', 'Fine.mp3'], ids=['text file', 'audio file'])
    def test_add_audio_file_instead_of_a_photo(self, get_auth_key, request, pet_file, name='Krosh',
                                               animal_type='rabbit', age='5'):
        """ Проверяем, что при создании нового питомца нельзя добавить ни текстовый, ни аудио файл вместо фото """
        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), f'images/{pet_file}').replace('\\', '/')

        start_time = time.time_ns()  # запускаем таймер
        # Добавляем питомца
        status, result, content, optional = pf.add_new_pet(get_auth_key, name, animal_type, age, pet_photo)
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
        assert result['pet_photo'] == ''
        assert res_time < 1000, 'Request - response longer than 1 sec'

        title = f'{request.node.name}\n{self.test_add_audio_file_instead_of_a_photo.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


    @pytest.mark.negative
    @pytest.mark.add_file
    @pytest.mark.parametrize('pet_file', ['wrong_photo.txt', 'Fine.mp3'], ids=['text file', 'audio file'])
    def test_failed_audio_file(self, get_auth_key, request, pet_file):
        """ Проверяем, что при обновлении фото питомца нельзя прикрепить ни текстовый файл, ни аудио файл вместо фото """

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), f'images/{pet_file}').replace('\\', '/')

        start_time = time.time_ns()  # запускаем таймер
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
        end_time = time.time_ns()  # останавливаем таймер
        res_time = (end_time - start_time) // 1_000_000

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 500
        assert res_time < 1000, 'Request - response longer than 1 sec'
        # assert result['name'] == name

        title = f'{request.node.name}\n{self.test_failed_audio_file.__doc__}\n'
        log_request(title, content, optional, result, rt=res_time)


@pytest.mark.negative
def test_get_api_key_for_invalid_password(request, email=valid_email, password=invalid_password):
    ''' Проверяем, что при вводе неправильного пароля нельзя получить API ключ '''

    start_time = time.time_ns()  # запускаем таймер
    # Отправляем запрос, ожидаем ошибку
    status, result, content, optional = pf.get_api_key(email, password)
    end_time = time.time_ns()  # останавливаем таймер
    res_time = (end_time - start_time) // 1_000_000

    assert status == 403
    assert res_time < 1000, 'Request - response longer than 1 sec'

    title = f'{request.node.name}\n{test_get_api_key_for_invalid_password.__doc__}\n'
    log_request(title, content, optional, result, rt=res_time)


@pytest.mark.negative
def test_get_api_key_for_invalid_email(request, email=invalid_email, password=valid_password):
    ''' Проверяем, что при вводе неправильного e-mail нельзя получить API ключ '''

    start_time = time.time_ns()  # запускаем таймер
    # Отправляем запрос, ожидаем ошибку
    status, result, content, optional = pf.get_api_key(email, password)
    end_time = time.time_ns()  # останавливаем таймер
    res_time = (end_time - start_time) // 1_000_000

    assert status == 403
    assert res_time < 1000, 'Request - response longer than 1 sec'

    title = f'{request.node.name}\n{test_get_api_key_for_invalid_email.__doc__}\n'
    log_request(title, content, optional, result, rt=res_time)


@pytest.mark.negative
@pytest.mark.parametrize('api_key', ['', generate_string(255), generate_string(1001), '1234567890'],
                         ids=['empty string', '255 symbols', '1001 symbols', 'numbers'])
def test_get_my_pet_info_with_wrong_key(request, api_key, filter='my_pets'):
    ''' Проверяем невозможность получения информации о питомцах, если указан неверный ключ '''

    start_time = time.time_ns()  # запускаем таймер
    # Отправляем запрос, ожидаем ошибку
    auth_key = {'key': api_key}

    status, result, content, optional = pf.get_list_of_pets(auth_key, filter)

    end_time = time.time_ns()  # останавливаем таймер
    res_time = (end_time - start_time) // 1_000_000

    assert status == 403
    assert res_time < 1000, 'Request - response longer than 1 sec'

    title = f"{request.node.name}\n{test_get_my_pet_info_with_wrong_key.__doc__}\n"
    log_request(title, content, optional, result, rt=res_time)