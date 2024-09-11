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
    """
    Класс взаимодействия с дроном
    Класс содержит метод получения статуса дрона
    Для удобства остальные методы рабрты с дроном вынесены в отдельный файл - strategy.py
    """
    def __init__(self, coordinates):
        self._coordinates = coordinates

    def drone_status(self):
        try:
            response = requests.get(f'{BASE_URL}/drone_status')
            if response.status_code == 200:
                logging.info(f"Получен статус тостояния от дрона: {response.json()}")
                return  response.json()['message']
            else:
                logging.info("Ошибка при отправке запроса:", response.status_code)
        except Exception as e:
            logging.info("Ошибка при подключении к серверу:", e)


def drone_control(coordinates):
    """
    Метод инициализируем дрона
    """
    drone = Drone(coordinates)
    drone_status = drone.drone_status()

    # Создаем экземпляры
    drone_controller = DronController()
    context = DroneContext()
    if drone_status == "Я на земле.":
        context.set_strategy(BaseDepartureStrategy())
        # Формируем список команд
        context.add_command(Takeoff(drone_controller))
        context.add_command(MoveForward(drone_controller, coordinates))

        # Возвращаем решение о выбранной миссии и список команд для дрона
        context.execute()

    elif drone_status == "Я в воздухе.":
        context.set_strategy(FlightChangeStrategy())
        # Формируем список команд
        context.add_command(MoveForward(drone_controller, coordinates))

        # Возвращаем решение о выбранной миссии и список команд для дрона
        context.execute()


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
            # Инициализируем управление дроном
            drone = drone_control(coordinates)
            # Сброс счетчика после отправки команды дрону
            camera_request_count[str(camera_index)] = 0

        return jsonify({'message': 'Уведомление получено'}), 200


app.run(debug=True, host='127.0.0.1', port=5000)