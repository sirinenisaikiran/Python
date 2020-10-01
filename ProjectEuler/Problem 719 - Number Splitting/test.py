import math
from datetime import datetime

Start_time = datetime.now()
N = 10 ** 12
for n in range(4,N+1):
    sqrt_of_n = math.sqrt(n) #duration 0:00:22.812134
    #sqrt_of_n = n ** 0.5 #duration 0:00:22.295261
    if sqrt_of_n - math.floor(sqrt_of_n) == 0:
        print(n)
End_time = datetime.now()
print("duration {}".format(End_time-Start_time))