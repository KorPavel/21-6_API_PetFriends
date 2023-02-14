# Задание 21.6 "Testing API PetFriends"
Продолжение задания 19.7.2 (+ fixture)  
1. Подумайте над вариантами тест-кейсов и напишите 10 различных тестов для данного REST API-интерфейса.  
2. Переделайте тесты, которые вы написали в модуле 19 так, чтобы они использовали фикстуру получения ключа API, а не делали это каждый раз внутри себя.

---

Объект тестирования: *[сайт "PetFriends"](https://petfriends.skillfactory.ru/)*  
API сайта: *[Flasgger](https://petfriends.skillfactory.ru/apidocs/)*  

### [Чек-листы проверок запросов API](https://docs.google.com/document/d/19Zi-HGKGmOGSEF2Vj2uyXNN5MaooKe_Y7DQB0I1Pe7c/edit?usp=drivesdk)  


#### Окружение: 
- OC Windows 10 Version 21H2   
- Google Chrome  Версия 109.0.5414.75, (64 бита)

В целях сокрытия конфиденциальной информации проекте используется файл `.env` (*не представлен*), для которого нужна библиотека "python-dotenv"
#### Пример содержания файла `.env`:
>valid_email = '`example@email.com`'  
>valid_password = '`QwErTy`'  

Перед запуском тестов требуется установить необходимые библиотеки командой:
   ```bash
   pip install -r requirements.txt
   ```
Для запуска тестов через терминал следует набрать команду:  
   ```bash
   pytest -v -s tests\test_pf_v2.py
   ```