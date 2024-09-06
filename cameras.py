from abc import ABC, abstractmethod
import time
import cv2
import logging
import threading
import requests  # Импортируем библиотеку для HTTP-запросов


logging.basicConfig(level=logging.INFO, filemode="w", format='%(name)s - %(levelname)s - %(message)s')

BASE_URL = 'http://localhost:5000'


class AbstractCamera(ABC):
    """
    Паттерн - Шаблонный метод (Template Method):
    Абстрактный Класс AbstractCamera задаёт общий интерфейс и структуру для всех камер,
    определяя абстрактные методы start, process_frame и detect_obstacle.
    Конкретные реализации этих методов выполняются в подклассах (SimpleStationaryCamera и его производные).
    Это позволяет избежать дублирования кода и обеспечить единообразие в обработке кадров.
    """
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.stop_flag = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def process_frame(self, frame):
        pass

    @abstractmethod
    def detect_obstacle(self, edges):
        pass


class SimpleStationaryCamera(AbstractCamera):
    """
    Класс описания работы конкретной простой стационарной камеры.
    Паттерн позволяет наже в коде вставить описание любой другой модели стационарной камеры.
    """
    def start(self):
        cap = cv2.VideoCapture(self.camera_index)
        while not self.stop_flag:
            ret, frame = cap.read()
            if not ret:
                break

            edges = self.process_frame(frame)
            self.detect_obstacle(edges)

            cv2.imshow(f'Камера {self.camera_index}', edges)

            if (cv2.getWindowProperty(f'Камера {self.camera_index}', cv2.WND_PROP_VISIBLE) < 1 or
                    cv2.waitKey(1) & 0xFF == ord('q')):#  этот код используется для завершения работы программы или
                                                # цикла, если окно камеры закрыто или пользователь нажал клавишу 'q'.
                self.stop_flag = True
                break

            time.sleep(0.05)

        cap.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        # Уменьшаем разрешение изображения в 2 раза
        frame_resized = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return edges

    def detect_obstacle(self, edges):
        if edges.sum() > 100000:
            logging.info(f'Камера {self.camera_index}: Объект обнаружен')
            self.send_alert_to_server()
        else:
            logging.info(f'Камера {self.camera_index}: Объект не обнаружен')

    def send_alert_to_server(self):
        # Отправляем POST-запрос на сервер с координатами камеры
        data = {
            'camera_index': self.camera_index,
            'coordinates': self.camera_coordinates
        }
        response = requests.post(f'{BASE_URL}/alert', json=data)
        if response.status_code == 200:
            logging.info(f'Уведомление отправлено на сервер: {response.json()}')
        else:
            logging.info(f'Ошибка при отправке уведомления на сервер: {response.status_code}')


class CameraFactory:
    """
    Паттерн фабрика - позволяет создавать объекты без необходимости указывать конкретный класс создаваемого объекта.
    В данном случае, CameraFactory отвечает за создание экземпляров различных классов камер на основе переданного типа.
    """
    @staticmethod
    def create_camera(camera_type):
        if camera_type == 'camera_1':
            return Camera1()
        elif camera_type == 'camera_2':
            return Camera2()
        elif camera_type == 'camera_3':
            return Camera3()
        elif camera_type == 'camera_4':
            return Camera4()
        raise ValueError(f"Unknown camera type: {camera_type}")


class Camera1(SimpleStationaryCamera):
    """
    Камера 1 (Левый верхний угол): (-250, 150)
    """
    def __init__(self):
        super().__init__(0)
        self.camera_coordinates = {"latitude": -250.0, "longitude": 150.0}


class Camera2(SimpleStationaryCamera):
    """
    Камера 2 (Правый верхний угол): (250, 150)
    """
    def __init__(self):
        super().__init__(1)
        self.camera_coordinates = {"latitude": 250.0, "longitude": 150.0}


class Camera3(SimpleStationaryCamera):
    """
    Камера 3 (Левый нижний угол): (-250, -150)
    """
    def __init__(self):
        super().__init__(2)
        self.camera_coordinates = {"latitude": -250.0, "longitude": -150.0}


class Camera4(SimpleStationaryCamera):
    """
    Камера 4 (Правый нижний угол): (250, -150)
    """
    def __init__(self):
        super().__init__(3)
        self.camera_coordinates = {"latitude": 250.0, "longitude": -150.0}


def run_camera(camera):
    camera.start()


if __name__ == "__main__":
    cameras = [
        CameraFactory.create_camera('camera_1')
        # Резервный код. Реализуется при наличии 4-х камер.
        # CameraFactory.create_camera('camera_1'),
        # CameraFactory.create_camera('camera_2'),
        # CameraFactory.create_camera('camera_3'),
        # CameraFactory.create_camera('camera_4')
    ]

    threads = []

    for camera in cameras:
        thread = threading.Thread(target=run_camera, args=(camera,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # Ожидание завершения всех потоков
