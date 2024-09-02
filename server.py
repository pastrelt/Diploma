import requests
from flask import Flask, request, jsonify, Response


app = Flask(__name__)



class Drone:
    def takeoff(self):
        try:
            response = requests.post('http://your-server-url/takeoff')  # Укажите URL вашего сервера
            if response.status_code == 200:
                print("Запрос на взлет успешно отправлен.")
            else:
                print("Ошибка при отправке запроса на взлет:", response.status_code)
        except Exception as e:
            print("Ошибка при подключении к серверу:", e)


app.run(debug=True, host='127.0.0.1', port=5000)
