from abc import ABC, abstractmethod
import requests
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO, filemode="w")
BASE_URL = 'http://localhost:5001'


# Реализуем паттерн Абстрактная Фабрика
# Конкретная реализация управления дроном
class DronController:
    """
    Класс управления дроном. Содержит методы для взлета, движения вперед и поворота.
    """
    def takeoff(self):
        """
        Передаем команду дрону на взлет.
        """
        altitude = {'altitude': 50.0}
        try:
            response = requests.post(f'{BASE_URL}/takeoff', json=altitude)
            response.raise_for_status()  # Проверка на ошибки HTTP
            logging.info(f"Получен ответ дрона на команду - взлет: {response.json()}")
            return response.json()['message']
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при отправке запроса: {e}")
            return None  # Возврат значения по умолчанию


    def move_forward(self, coordinates):
        """
        Передаем дрону команду полета по заданным координатам.
        """
        try:
            response = requests.post(f'{BASE_URL}/move_forward', json=coordinates)
            response.raise_for_status()  # Проверка на ошибки HTTP
            logging.info(f"Получен ответ дрона на команду - взлет: {response.json()}")
            return response.json()['message']
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при отправке запроса: {e}")
            return None

    def move_back(self, coordinates):
        """
        Передаем дрону команду полета по заданным координатам (движение задом).
        """
        try:
            response = requests.post(f'{BASE_URL}/move_back', json=coordinates)
            response.raise_for_status()  # Проверка на ошибки HTTP
            logging.info(f"Получен ответ дрона на команду - взлет: {response.json()}")
            return response.json()['message']
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при отправке запроса: {e}")
            return None

    def turn(self, degree: float):
        """
        Передаем дрону команду полета на поворот.
        """
        try:
            response = requests.post(f'{BASE_URL}/turn', json=degree)
            response.raise_for_status()  # Проверка на ошибки HTTP
            logging.info(f"Получен ответ дрона на команду - взлет: {response.json()}")
            return response.json()['message']
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при отправке запроса: {e}")
            return None
    def landing(self):
        """
        Передаем дрону команду на посадку.
        """
        try:
            response = requests.get(f'{BASE_URL}/landing')
            response.raise_for_status()  # Проверка на ошибки HTTP
            logging.info(f"Получен ответ дрона на команду - посадка: {response.json()}")
            return response.json()['message']
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при отправке запроса: {e}")
            return None  # Возврат зна
        logging.info("Дрон приземлился")


# Реализация патерна Сомманда
# разделяем наши команды от логики управления нашими миссиями
class ICommand(ABC):# интерфейс
    @abstractmethod
    def execute(self):
        pass


# Взлет
class Takeoff(ICommand):
    def __init__(self, drone: DronController):
        self.__drone = drone

    def execute(self):
        self.__drone.takeoff()


# Движение вперед
class MoveForward(ICommand):
    def __init__(self, drone: DronController, coordinates):
        self.__drone = drone
        self.__coordinates = coordinates

    def execute(self):
        self.__drone.move_forward(self.__coordinates)


# Движение назад
class MoveBack(ICommand):
    def __init__(self, drone: DronController, coordinates):
        self.__drone = drone
        self.__coordinates = coordinates

    def execute(self):
        self.__drone.move_back(self.__coordinates)


# Поворот
class Turn(ICommand):
    def __init__(self, drone: DronController, degree: float):
        self.__drone = drone
        self.__degree = degree

    def execute(self):
        self.__drone.turn(self.__degree)


# Посадка
class Landing(ICommand):
    def __init__(self, drone: DronController):
        self.__drone = drone

    def execute(self):
        self.__drone.landing()


# Реализуем патерн Стратегия
# Интерфейс стратегии полета, определяет метод execute
class IFlightStrategy(ABC):
    @abstractmethod
    def execute(self, commands: list):
        """
        Метод для выполнения списка команд в рамках стратегии.
        :param commands: Список команд для выполнения.
        """
        pass


# Стратегия вылета с базовой точки
class BaseDepartureStrategy(IFlightStrategy):
    def execute(self, commands: list):
        logging.info(f'Выбрана стратеия: "Взлет с базы"')
        for command in commands:
            command.execute()
        return commands


# Стратегия изменения маршрута.
class FlightChangeStrategy(IFlightStrategy):
    def execute(self, commands: list):
        logging.info(f'Выбрана стратеия: "Изменение маршрута"')
        # for command in commands:
        #     command.execute()
        return commands


# Контекст для управления стратегиями полета дрона
class DroneContext:
    def __init__(self, strategy: IFlightStrategy = None):
        self.__strategy = strategy  # Текущая стратегия полета
        self.__commands = []  # Список команд

    def set_strategy(self, strategy: IFlightStrategy):
        """
        Устанавливает стратегию полета.
        :param strategy: Объект, реализующий интерфейс IFlightStrategy.
        """
        self.__strategy = strategy

    def add_command(self, command: ICommand):
        """
        Добавляет команду в список для выполнения.
        :param command: Объект, реализующий интерфейс ICommand.
        """
        self.__commands.append(command)

    def execute(self):
        """
        Выполняет все команды, используя текущую стратегию полета.
        После выполнения команды очищает список.
        """
        self.__strategy.execute(self.__commands)
        self.__commands.clear()
