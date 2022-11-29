import pytest
import time
from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()

""" Фикстура получает ключ авторизации с валидными данными и передаёт его тесты """
@pytest.fixture(scope='class', autouse=True)
def get_auth_key():
    """ Отравляем запрос и сохраняем полученный ответ с кодом статуса в status,
        а результат в auth_key """
    status, auth_key, _, _ = pf.get_api_key(email=valid_email, passwd=valid_password)

    assert status == 200
    assert 'key' in auth_key
    return auth_key

""" Фикстура удаляет тестовые данные (созданных в процессе тестирования питомцев) 
после прохождения каждого теста """
@pytest.fixture(autouse=True)
def delete_test_pets(get_auth_key):
    yield
    _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')
    while len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        pf.delete_pet(get_auth_key, pet_id)
        _, my_pets, _, _ = pf.get_list_of_pets(get_auth_key, 'my_pets')


""" Фикстура производит подсчёт времени выполнения каждого теста. 
Результаты аккумулирует в файле Timebook.txt, а также выводит в 
консоль после каждого теста """
@pytest.fixture(autouse=True)
def time_delta_teardown(request):
    # БЛОК SETUP
    # создаём блокнот для учёта времени
    with open('Timebook.txt', 'a', encoding='utf8') as file:
        file.write(f'* {request.node.name}\n')  # request.node.name - получаем имя запускааемого теста
    start_time = time.time_ns() # запускаем таймер
    yield

    # БЛОК TEARDOWN:
    end_time = time.time_ns() # останавливаем таймер
    res_time = (end_time - start_time) // 1000000
    with open("Timebook.txt", 'a', encoding='utf8') as file:
        file.write(f"> Время выполнения теста: {res_time / 1000} сек\n\n")
    # Выводим результат в консоль:
    print(f"\n* {request.node.name}\n> Время выполнения теста: "
          f"{res_time}мс ({res_time / 1000}сек)")
