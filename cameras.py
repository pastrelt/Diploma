from abc import ABC, abstractmethod
import cv2


BASE_URL = 'http://localhost:5000'

class AbstractCamera(ABC):
    """
    Паперн - Абстрактная фабрика
    Абстрактный Класс описания камер наблюдения.
    Содержит методы: работа камеры,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
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


class LeftFrontCamera(AbstractCamera):
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



class Camera_2(ICameraFactory):
    def camera_operation(self):
        pass

