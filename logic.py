import datetime
import time

work_session = []
def start_work(task_name):
    start_time = datetime.datetime.now()
    return {'task_name': task_name, 'start_time': start_time, 'end_time': None, 'duration': None}

def end_work(x):
    end_time = datetime.datetime.now()
    duration = end_time - x['start_time']
    x['end_time'] = end_time
    x['duration'] = duration

    work_session.append(x)
    return x

def total_hours():
    total_duration = datetime.timedelta()
    for x in work_session:
        total_duration += x['duration']
    print(total_duration)

print("start")
work = start_work("starting")
time.sleep(2)
print("end")
end_work(work)
print("total:")
total_hours()
    