import time
import requests
import logging
from flask import Flask, request, jsonify, Response


logging.basicConfig(level=logging.INFO, filemode="w", format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

BASE_URL = 'http://localhost:5000'


class Drone:
    status_drone = True# дрон на земле

    @app.route("/receive_alert", methods=["POST"])
    def receive_alert():
        """
        Mетод передает статус дрона
        :return: status_drone
        """
        if Drone.status_drone:
            return jsonify({"message": "Дрон на земле."})
        else:
            return jsonify({"message": "Дрон в полете."})




    # def update_detected(self, detected):
    #     self.detected = detected
    #     if detected:
    #         self.request_takeoff()
    #
    # def request_takeoff(self):
    #     try:
    #         response = requests.post('BASE_URL/takeoff')
    #         if response.status_code == 200:
    #             logging.info("Запрос на взлет успешно отправлен.")
    #         else:
    #             logging.info("Ошибка при отправке запроса на взлет:", response.status_code)
    #     except Exception as e:
    #         logging.info("Ошибка при подключении к серверу:", e)


app.run(debug=True, host='127.0.0.1', port=5001)