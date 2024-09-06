import requests
import logging
from strategy import *
from flask import Flask, request, jsonify, Response


logging.basicConfig(level=logging.INFO, filemode="w", format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

BASE_URL = 'http://localhost:5001'
# Словарь для хранения счетчиков запросов от камер (ключ - номер камеры, значение - количество пришедших сообщений с камеры)
camera_request_count = {
    '0': 0,
    '1': 0,
    '2': 0,
    '3': 0
}


class Drone:
    def __init__(self, coordinates):
        self._coordinates = coordinates

    def receive_alert(self):
        try:
            response = requests.post(f'{BASE_URL}/receive_alert')
            if response.status_code == 200:
                drone_status = response.json()['message']
                logging.info(f"Получен статус тостояния от дрона: {response.json()}")
                # Передаем статус дрона для определения стратегии полетного задания
                return strategy.drone_strategy_selection(drone_status, self._coordinates)
            else:
                logging.info("Ошибка при отправке запроса:", response.status_code)
        except Exception as e:
            logging.info("Ошибка при подключении к серверу:", e)


class Cameras:
    """
    Класс взаимодействия с камерой
    """
    @app.route("/alert", methods=["POST"])
    def alert():
        """
        Метод обрабатывае запрос камеры и если он подтверждается неоднократно (>100) отправляет дрон
        для съемки объекта нарушения, передавая координаты камеры.
        """
        global camera_request_count
        data = request.get_json()
        # Проверка наличия необходимых данных
        if 'camera_index' not in data or 'coordinates' not in data:
            logging.error('Некорректные данные: %s', data)
            return jsonify({'error': 'Некорректные данные'}), 400

        camera_index = data['camera_index']
        coordinates = data['coordinates']

        # Увеличение счетчика запросов для соответствующей камеры
        camera_request_count[str(camera_index)] += 1
        # logging.info(f'Получено уведомление от камеры {camera_index} с координатами {coordinates}. '
        #              f'Текущий счетчик: {camera_request_count[str(camera_index)]}')

        # Проверка, превышает ли счетчик 100
        if camera_request_count[str(camera_index)] > 100:
            # Инициализируем дрона
            drone = Drone(coordinates)
            drone.receive_alert()
            # Сброс счетчика после отправки команды дрону
            camera_request_count[str(camera_index)] = 0

        return jsonify({'message': 'Уведомление получено'}), 200

app.run(debug=True, host='127.0.0.1', port=5000)