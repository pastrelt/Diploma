from abc import ABC, abstractmethod
import cv2


class ICameraFactory(ABC):
    """
    Паперн - Абстрактная фабрика
    Абстрактный Класс описания камер наблюдения.
    Содержит методы: работа камеры, поворот камеры, вывод камеры
    """
    @abstractmethod
    def camera_operation(self):
        global stop_flag
        cap = cv2.VideoCapture(n_came)
        while not stop_flag:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)

            if edges.sum() > 100000:
                drone.update_detected(True)
            else:
                drone.update_detected(False)

            cv2.imshow('Обнаружение препятствия', edges)

            if (cv2.getWindowProperty('Обнаружение препятствия', cv2.WND_PROP_VISIBLE) < 1 or
                    cv2.waitKey(1) & 0xFF == ord('q')):
                stop_flag = True
                break
            time.sleep(0.05)
        cap.release()
        cv2.destroyAllWindows()


class Camera_1(ICameraFactory):
    def camera_operation(self):

