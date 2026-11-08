import datetime
import time

user_input = input("Start time:")
x = datetime.datetime.strptime(user_input, "%H%M")
print(x.time())

user_input = input("End time:")
y = datetime.datetime.strptime(user_input, "%H%M")
print(y.time())

z = y - x

print("Time Worked:" ,z)