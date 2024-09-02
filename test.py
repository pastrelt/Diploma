from abc import ABC, abstractmethod
import time
import cv2


BASE_URL = 'http://localhost:5000'

class AbstractCamera(ABC):
    """
    Паттерн - Абстрактная фабрика
    Абстрактный Класс описания камер наблюдения.
    Содержит методы: запуск камеры, обработка изображения, обнаружение объекта
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
    Класс описания конкретной стационарной камеры наблюдения.
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
                    cv2.waitKey(1) & 0xFF == ord('q')):
                self.stop_flag = True
                break

            time.sleep(0.05)

        cap.release()
        cv2.destroyAllWindows()

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)# преобразование в оттенки серого
        edges = cv2.Canny(gray, 100, 200)# обнаружение краев
        return edges

    def detect_obstacle(self, edges):
        if edges.sum() > 100000:
            print(f'Камера {self.camera_index}: Объект обнаружен')
        else:
            print(f'Камера {self.camera_index}: Объект не обнаружен')



class ComplexDroneCamera(AbstractCamera):
    """
    Класс описания конкретной камеры размещенной на дроне.
    """
    def start(self):
        pass

    def process_frame(self, frame):
        pass

    def detect_obstacle(self, edges):
        pass


class CameraFactory:
    """
    Петтерн фабрика - позволяет создавать объекты без необходимости указывать конкретный класс создаваемого объекта.
    В данном случае, CameraFactory отвечает за создание экземпляров различных классов камер на основе переданного типа.
    Создание фабрики для камер
    """
    @staticmethod
    def create_camera(camera_type):
        if camera_type == 'camera1':
            return Camera1()
        elif camera_type == 'camera2':
            return Camera2()
        elif camera_type == 'camera3':
            return Camera3()
        elif camera_type == 'camera4':
            return Camera4()
        raise ValueError(f"Unknown camera type: {camera_type}")

    # @staticmethod
    # def create_camera(camera_type, camera_index):
    #     if camera_type == 'simple':
    #         return SimpleCamera(camera_index)
    #     # Здесь можно добавить другие типы камер
    #     raise ValueError(f"Unknown camera type: {camera_type}")

class Camera1(SimpleStationaryCamera):
    """
    Камера 1 (Левый верхний угол): (-250, 150)
    """
    def __init__(self):
        super().__init__(0)
        self.camera_coordinates = (-250, 150)


class Camera2(SimpleStationaryCamera):
    """
    Камера 2 (Правый верхний угол): (250, 150)
    """
    def __init__(self):
        super().__init__(1)
        self.camera_coordinates = (250, 150)

class Camera3(SimpleStationaryCamera):
    """
    Камера 3 (Левый нижний угол): (-250, -150)
    """
    def __init__(self):
        super().__init__(2)
        self.camera_coordinates = (-250, -150)

class Camera4(SimpleStationaryCamera):
    """
    Камера 4 (Правый нижний угол): (250, -150)
    """
    def __init__(self):
        super().__init__(3)
        self.camera_coordinates = (250, -150)


if __name__ == "__main__":
    camera1 = CameraFactory.create_camera('camera1')

    # Запуск камер
    camera1.start()
