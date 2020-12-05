from time import sleep, time
from random import random

t = time()

while time() - t < 5:
    print(time() - t)
    sleep(random() * 2)
