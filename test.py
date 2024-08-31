import cv2
import time
import requests


class Drone:
    def __init__(self):
        self.detected = False

    def update_detected(self, detected):
        self.detected = detected
        if detected:
            self.request_takeoff()

    def request_takeoff(self):
        try:
            response = requests.post('http://your-server-url/takeoff')  # Укажите URL вашего сервера
            if response.status_code == 200:
                print("Запрос на взлет успешно отправлен.")
            else:
                print("Ошибка при отправке запроса на взлет:", response.status_code)
        except Exception as e:
            print("Ошибка при подключении к серверу:", e)


class Camera:
    def __init__(self, drone, camera_index):
        self.drone = drone
        self.camera_index = camera_index
        self.stop_flag = False

    def start(self):
        cap = cv2.VideoCapture(self.camera_index)
        while not self.stop_flag:
            ret, frame = cap.read()
            if not ret:
                break

            edges = self.process_frame(frame)
            self.detect_obstacle(edges)

            cv2.imshow('Обнаружение препятствия', edges)

            if (cv2.getWindowProperty('Обнаружение препятствия', cv2.WND_PROP_VISIBLE) < 1 or
                    cv2.waitKey(1) & 0xFF == ord('q')):
                self.stop_flag = True
                break

            time.sleep(0.05)

        cap.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return edges

    def detect_obstacle(self, edges):
        if edges.sum() > 100000:
            self.drone.update_detected(True)
        else:
            self.drone.update_detected(False)


# Пример использования
if __name__ == "__main__":
    drone = Drone()
    camera_index = 0  # Укажите индекс вашей камеры
    camera = Camera(drone, camera_index)
    camera.start()
