import sys
from datetime import datetime

def getDetails(line):
    dArray = line.split()
    timestamp = dArray[0] + " " + dArray[1] + " " + dArray[2]
    device = dArray[3][1:-1]
    code = dArray[4]
    state = dArray[6]
    return timestamp, device, code, state

def timeDifference(timeDic):
    # t1 is before t2
    t1 = timeDic.get("ON", -1)
    t2 = timeDic.get("OFF", -1)
    if t1 == -1:
        return -1
    if t2 == -1:
        return "currently running"
    
    d1 = datetime.strptime(t1, "%b %d %H:%M:%S:%f")
    d2 = datetime.strptime(t2, "%b %d %H:%M:%S:%f")
    diff = d2 - d1
    days = "" if diff.days == 0 else str(diff.days) + " days, "
    seconds = str(diff.seconds) + " seconds"
    return days + seconds

try:
    fileName = sys.argv[1]
except:
    fileName = input("Input a file name:")

# read file
with open("./" + fileName, "r") as f:
    lines = f.readlines()
    devicesTime = {}
    errors = {}
    for line in lines:
        timestamp, device, code, state = getDetails(line)
        if state == "ON":
            timeDic = devicesTime.get(device, {})
            timeDic["ON"] = timestamp
            devicesTime[device] = timeDic
        if state == "ERR":
            timeList = errors.get(device, [])
            timeList.append(timestamp)
            errors[device] = timeList
        if state == "OFF":
            timeDic = devicesTime.get(device, {})
            timeDic["OFF"] = timestamp
            devicesTime[device] = timeDic

    for device in sorted(devicesTime.keys()):
        diff = timeDifference(devicesTime[device])
        
        if diff == -1: continue
        print("Device", device, "was on for", diff + ".")
        if errors.get(device, -1) != -1:
            print("Device", device, "had following error events:")
            for timestamp in errors[device]:
                print("\t", timestamp)
        else:
            print("Device", device, "had no error events.")
