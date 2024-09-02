import time
import requests
from flask import Flask, request, jsonify, Response


app = Flask(__name__)

BASE_URL = 'http://localhost:5000'


class Drone:
    def __init__(self):
        self.detected = False

    def update_detected(self, detected):
        self.detected = detected
        if detected:
            self.request_takeoff()

    def request_takeoff(self):
        try:
            response = requests.post('BASE_URL/takeoff')
            if response.status_code == 200:
                print("Запрос на взлет успешно отправлен.")
            else:
                print("Ошибка при отправке запроса на взлет:", response.status_code)
        except Exception as e:
            print("Ошибка при подключении к серверу:", e)


app.run(debug=True, host='127.0.0.1', port=5001)