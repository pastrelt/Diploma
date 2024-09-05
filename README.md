Проект представляет собой веб-приложение, разработанного с 
использованием языка программирования Python и современных веб-технологий. 
Веб-сайт включает в себя автономно работающий интерфейс, 
взаимодействующий с серверной частью и дроном через API-интерфейсы. 
Основное внимание уделяется масштабируемости, безопасности и
производительности системы.

Цель проекта: Охрана территории.
Данный проект реализует сильные стороны стационарных и 
мобильных видео устройств при их совместном использовании.
Видео камеры, расположенные стационарно, в случае обнаружения
нарушителя передают сигнал на сервер, который высылает 
дрона в точку обнаружения, для точной фиксации данных
нарушителя.

Для старта проекта используется:
Python - 3.12.0

Файл запуска - start.py
Проект состоит из файлов:
start.py - файл запуска программы
cameras.py - работа стационактых камер
server.py - работа сервера
drone.py - работа дрона

сервер:
Flask-3.0.3

библиотеки
abc - модуль abc (Abstract Base Classes, Абстрактные Базовые Классы) в Python
    позволяет разрабатывать код, который указывает, какие методы должны быть 
    реализованы его подклассами.
cv2 - opencv-python-4.10.0.84 открытая библиотека для работы с алгоритмами 
    компьютерного зрения, машинным обучением и обработкой изображений. 
time - модуль для работы со временем в Python.
requests - HTTP-библиотека для Python.
threading - модуль  является одним из способов реализации многопоточности в Python.
logging -  встроенный модуль logging , применяемый для решения задач логирования.