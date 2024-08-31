import concurrent.futures
import cv2
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

stop_flag = False

class Drone:
    def __init__(self):
        self.__altitude = 0
        self.__obstacle_detected = False

    def update_altitude(self, new_altitude):
        self.__altitude = new_altitude

    def update_detected(self, status):
        self.__obstacle_detected = status

    def control(self):
        if self.__obstacle_detected:
            logging.info("Обнаружено препятствие! Зависаем...")
        elif self.__altitude < 10:
            logging.info("Набираем высоту")
            self.update_altitude(self.__altitude + 1)
        else:
            logging.info("Удержание высоты")


def read_altimeter(drone: Drone):
    global stop_flag
    while not stop_flag:
        altitude = random.uniform(5.0, 15.0)
        drone.update_altitude(altitude)
        logging.info(f"Высота: {altitude:.2f}")
        time.sleep(0.1)


def control(drone: Drone):
    global stop_flag
    while not stop_flag:
        drone.control()
        time.sleep(0.1)

def read_video(drone: Drone):
    global stop_flag
    cap = cv2.VideoCapture(0)
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
                cv2.waitKey(1) & 0xFF == ord('q')) :
            stop_flag = True
            break
        time.sleep(0.05)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    drone = Drone()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        altimeter_future = executor.submit(read_altimeter, drone)
        control_future = executor.submit(control, drone)
        video_future = executor.submit(read_video, drone)

        # read_video(drone)

    concurrent.futures.wait([video_future, altimeter_future, control_future])