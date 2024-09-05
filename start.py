import subprocess
from cameras import *


subprocess.Popen(['python', 'server.py'])
subprocess.Popen(['python', 'drone.py'])

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
print("Получилось!")
