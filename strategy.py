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
        logging.info("Дрон взлетает...")

    def move_forward(self, distance: float):
        logging.info(f"Дрон летит вперед на {distance} метров")

    def move_back(self, distance: float):
        logging.info(f"Дрон летит назад на {distance} метров")

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
    def __init__(self, drone: DronController, distance: float):
        self.__drone = drone
        self.__distance = distance

    def execute(self):
        self.__drone.move_forward(self.__distance)


# Движение назад
class MoveBack(ICommand):
    def __init__(self, drone: DronController, distance: float):
        self.__drone = drone
        self.__distance = distance

    def execute(self):
        self.__drone.move_back(self.__distance)


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


# Стратегия разведывательной миссии
class ReconMissionStrategy(IFlightStrategy):
    def __init__(self, secret_key, mission):
        self._secret_key = secret_key
        self._mission = mission

    def execute(self, commands: list, token=None):
        # Выполняет разведывательную миссию, выполняя все команды в списке
        logging.info(f"Начало выполнения разведывательной миссии")
        # '''
        #  Учитывая, что декораторы в Python применяются к функциям во время определения,
        #     а не во время вызова, поэтому нельзя использовать self напрямую в декораторе.
        #     Вместо этого можно создать обертку вокруг метода execute, чтобы передать self.secret_key
        #     в декоратор.
        # '''
        # # Обертываем метод execute в декоратор
        # decorated_execute = SafetyCheck(self._secret_key, self._mission)(self._execute)
        # decorated_execute(commands=commands, token=token)
        logging.info(f"Конец миссии")

    def _execute(self, commands, token):
        for command in commands:
            command.execute()


# Стратегия патрульной миссии
class PatrolMissionStrategy(IFlightStrategy):
    def __init__(self, n_patrols: int, secret_key, mission):
        self._n_patrols = n_patrols# количество циклов патрулирования
        self._secret_key = secret_key
        self._mission = mission

    def execute(self, commands: list, token=None):
        # Выполняет патрульную миссию, повторяя все команды в списке заданное количество раз
        logging.info(f"Начало выполнения миссии патрулирования")

        # # Обертываем метод execute в декоратор
        # decorated_execute = SafetyCheck(self._secret_key, self._mission)(self._execute)
        # decorated_execute(commands=commands, token=token)
        logging.info(f"Конец миссии")

    def _execute(self, commands, token):
        for i in range(self._n_patrols):
            for command in commands:
                command.execute()
            logging.info(f"Облет №{i+1} завершен.")


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

    def execute(self, token=None):
        """
        Выполняет все команды, используя текущую стратегию полета.
        После выполнения команды очищает список.
        """
        self.__strategy.execute(self.__commands, token)
        self.__commands.clear()