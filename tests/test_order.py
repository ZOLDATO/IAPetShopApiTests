import allure
import pytest
import requests
import jsonschema
from .schemas.order_schema import ORDER_SCHEMA, INVENTORY_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('Store')
class TestOrder:

    # Тест 42
    @allure.title('Размещение заказа')
    def test_create_order(self):
        with allure.step('Подготовка данных для размещения заказа'):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step(f'Отправка запроса на размещение заказа'):
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()

        with allure.step('Проверка статуса ответа и соответствия схеме'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожижаемым'
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step('Проверка параметров размещенного заказа в ответе'):
            assert response_json["id"] == payload["id"], "id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == payload["petId"], "id питомца не совпадает с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "количество питомцев не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "статус заказа не совпадает с ожидаемым"
            assert response_json["complete"] == payload["complete"], "завершенность заказа не совпадает с ожидаемым"

    # Тест 43
    @allure.title('Получение информации о заказе по ID')
    def test_get_order_by_id(self, create_order):
        with allure.step('Получение ID размещенного заказа'):
            order_id = create_order["id"]

        with allure.step('Отправка запроса на получение информации о заказе по ID'):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа и id заказа'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'
            assert response.json()["id"] == order_id, "ID заказа не совпадает"

    # Тест 44
    @allure.title('Удаление заказа по ID')
    def test_delete_order(self, create_order):
        with allure.step('Получение ID размещенного заказа'):
            order_id = create_order["id"]

        with allure.step('Отправка запроса на удаление заказа'):
            response = requests.delete(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа на запрос по удалению заказа'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'

        with allure.step('Отправка запроса на получение данных удаленного заказа'):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step('Проверка статуса ответа на запрос по получению данных удаленного заказа'):
            assert response.status_code == 404, 'Код ответа не совпадает с ожидаемым'

    # Тест 45
    @allure.title('Попытка получить информацию о несуществующем заказе')
    def test_get_nonexistent_order(self):
        with allure.step('Отправка запроса на получение информации о несуществующем заказе'):
            response = requests.get(url=f'{BASE_URL}/store/order/9999')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпадает с ожижаемым'

        with allure.step('Проверка текстового содержимого ошибки'):
            assert response.text == 'Order not found', 'Текст ошибки не совпал с ожидаемым'

    # Тест 46
    @allure.title('Получение инвентаря магазина')
    def test_get_inventory(self):
        with allure.step(f'Отправка запроса на получение инвентаря магазина'):
            response = requests.get(url=f'{BASE_URL}/store/inventory')
            response_json = response.json()

        with allure.step('Проверка статуса и содержимого ответа на запрос по получению инвентаря магазина'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'
            jsonschema.validate(response_json, INVENTORY_SCHEMA)
