from abc import ABC, abstractmethod
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO, filemode="w")

# Реализуем патерн Абстрактная Фабрика
# Конкретная реализация управления дроном
class DronController:
    """
    Класс управления дроном. Содержит методы для взлета, движения вперед и поворота.
    """
    def takeoff(self):
        """
        Команда для взлета дрона.
        """
        logging.info("Дрон взлетает на 50 метров")

    def move_forward(self, coordinates):
        logging.info(f"Дрон летит по координатам {coordinates}")

    def move_back(self, coordinates):
        logging.info(f"Дрон летит на базу")

    def turn(self, degree: float):
        logging.info(f"Поворачиваем на {degree} градусов")

    def landing(self):
        """
        Команда посадки дрона.
        """
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
        # for command in commands:
        #     command.execute()
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


def drone_strategy_selection(drone_status, coordinates):
    """
    Метод выбира стратегии
    :param drone_status, coordinates:
    :return:
    """
    # Создаем экземпляры
    drone_controller = DronController()
    context = DroneContext()
    if drone_status == "Я на земле.":
        # Стратегия вылета с базовой точки
        context.set_strategy(BaseDepartureStrategy())

        # Формируем список команд
        context.add_command(Takeoff(drone_controller))
        context.add_command(MoveForward(drone_controller, coordinates))

        # Выполняем миссию
        context.execute()

    elif drone_status == "Я в воздухе.":
        # Стратегия изменения маршрута.
        context.set_strategy(FlightChangeStrategy())

        # Формируем список команд
        context.add_command(MoveForward(drone_controller, coordinates))

        # Выполняем миссию
        context.execute()