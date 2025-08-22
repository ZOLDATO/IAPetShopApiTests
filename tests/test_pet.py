import allure
import requests
import jsonschema
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('Pet')
class TestPet:
    @allure.title('Попытка удалить несуществующего питомца')
    def test_delete_nonexistent_pet(self):
        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            response = requests.delete(url=f'{BASE_URL}/pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожижаемым'

        with allure.step('Проверка текстового содержимого ошибки'):
            assert response.text == 'Pet deleted', 'Текст ошибки не совпал с ожидаемым'

    @allure.title('Попытка обновить несуществующего питомца')
    def test_update_nonexistent_pet(self):
        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"
                       }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпадает с ожижаемым'

        with allure.step('Проверка текстового содержимого ошибки'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    @allure.title('Попытка получить информацию о несуществующем питомце')
    def test_get_nonexistent_pet(self):
        with allure.step('Отправка запроса на получение информации о несуществующем питомце'):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпадает с ожижаемым'

        with allure.step('Проверка текстового содержимого ошибки'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    @allure.title('Добавление нового питомца')
    def test_add_pet(self):
        with allure.step('Подготовка данных для создания питомца'):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"
                       }

        with allure.step('Отправка запроса на создание питомца'):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожижаемым'
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step('Проверка параметров питомца в ответе'):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус питомца не совпадает с ожидаемым"

    @allure.title('Добавление нового питомца c полными данными')
    def test_add_pet_full_info(self):
        with allure.step('Подготовка полных данных для создания питомца'):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0,
                        "name":
                            "string"
                    }
                ],
                "status": "available"
            }

        with allure.step('Отправка запроса на создание питомца'):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидемым'
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step('Проверка параметров питомца в ответе'):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "имя питомца не совпадает с ожидаемым"
            assert response_json["category"] == payload["category"], "категория питомца не совпадает с ожидаемым"
            assert response_json["photoUrls"] == payload[
                "photoUrls"], "ссылки на фото питомца не совпадают с ожидаемыми"
            assert response_json["tags"] == payload["tags"], "бирки питомца не совпадают с ожидаемыми"
            assert response_json["status"] == payload["status"], "статус питомца не совпадает с ожидаемым"

    @allure.title('Получение информации о питомце по ID')
    def test_get_pet_by_id(self, create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet["id"]

        with allure.step('Отправка запроса на получение информации о питомце по ID'):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step('Проверка статуса ответа и id питомца'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'
            assert response.json()["id"] == pet_id, "ID питомца не совпадает"

    @allure.title('Обновление информации о питомце')
    def test_update_pet(self, create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet["id"]

        with allure.step('Подготовка данных и отправка запроса на обновление данных питомца'):
            payload = {"id": pet_id,
                       "name": "Buddy Updated",
                       "status": "sold"
                       }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)

        with allure.step('Проверка статуса ответа и данных питомца'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'
            assert response.json()["id"] == pet_id, 'ID питомца не совпадает'
            assert response.json()["name"] == "Buddy Updated", 'Имя питомца не совпадает'
            assert response.json()["status"] == "sold", 'Статус питомца не совпадает'

    @allure.title('Удаление питомца по ID')
    def test_delete_pet(self, create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet["id"]

        with allure.step('Отправка запроса на удаление питомца'):
            response = requests.delete(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step('Проверка статуса ответа на запрос по удалению питомца'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'

        with allure.step('Отправка запроса на получение данных удаленного питомца'):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step('Проверка статуса ответа на запрос по получению данных удаленного питомца'):
            assert response.status_code == 404, 'Код ответа не совпадает с ожидаемым'