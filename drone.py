import time
import requests
import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, filemode="w", format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

BASE_URL = 'http://localhost:5000'


class Drone:
    status_drone = True  # дрон на земле

    @staticmethod
    @app.route("/drone_status", methods=["GET"])
    def drone_status():
        """
        Метод передает статус дрона
        :return: status_drone
        """
        logging.info("Получен запрос о состоянии дрона")
        if Drone.status_drone:
            return jsonify({"message": "Я на земле."}), 200
        else:
            return jsonify({"message": "Я в воздухе."}), 200

    @staticmethod
    @app.route("/takeoff", methods=["POST"])
    def takeoff():
        """
        Метод взлета. Дрон получает команду в случае если он находится на земле.
        """
        command = request.get_json()['altitude']
        if command:
            logging.info("Получена команда на взлет.")
            Drone.status_drone = False  # Дрон в воздухе
            return jsonify({'message': f'Взлетел на {command} метров.'}), 200
        else:
            logging.error('Некорректные данные: %s', command)
            return jsonify({'error': 'Некорректные данные'}), 400

    @staticmethod
    @app.route("/move_forward", methods=["POST"])
    def move_forward():
        """
        Метод движения дрона вперед.
        """
        command = request.get_json()
        if command:
            logging.info("Получена команда двигаться вперед.")
            return jsonify({'message': f'Двигаюсь к координатам, веду съемку: {command}'}), 200
        else:
            logging.error('Некорректные данные: %s', command)
            return jsonify({'error': 'Некорректные данные'}), 400

    @staticmethod
    @app.route("/move_back", methods=["POST"])
    def move_back():
        """
        Метод движения дрона назад без разворота.
        """
        command = request.get_json()
        if command:
            logging.info("Получена команда двигаться назад.")
            return jsonify({'message': f'Двигаюсь к координатам: {command}'}), 200
        else:
            logging.error('Некорректные данные: %s', command)
            return jsonify({'error': 'Некорректные данные'}), 400

    @staticmethod
    @app.route("/turn", methods=["POST"])
    def turn():
        """
        Метод поворота дрона.
        """
        command = request.get_json()['degree']
        if command:
            logging.info("Получена команда повернуть.")
            return jsonify({'message': f'Повернул на: {command} градусов.'}), 200
        else:
            logging.error('Некорректные данные: %s', command)
            return jsonify({'error': 'Некорректные данные'}), 400

    @staticmethod
    @app.route("/landing", methods=["GET"])
    def landing():
        """
        Метод для посадки дрона.
        """
        logging.info("Получена команда на посадку.")
        Drone.status_drone = True  # Дрон на земле
        return jsonify({'message': 'Посадка выполнена.'}), 200


app.run(debug=True, host='127.0.0.1', port=5001)