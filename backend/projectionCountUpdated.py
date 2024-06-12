from flask import Flask, request
import json
import datetime
from datetime import datetime
import math
from backend.RecentValidTimestamp import getValidTimestamps

app = Flask(__name__)


# function converting all the time units to minutes.
def convertTimeMinutes(expireTime):
    value = int(expireTime["value"])
    if expireTime["unit"] == "hours":
        return int(expireTime["value"]) * 60
    elif expireTime["unit"] == "DAILY" or expireTime["unit"] == "days":
        return int(expireTime["value"]) * 24 * 60
    elif expireTime["unit"] == "WEEKLY" or expireTime["unit"] == "weeks":
        return int(expireTime["value"]) * 24 * 7 * 60
    elif expireTime["unit"] == "MONTHLY" or expireTime["unit"] == "months":
        return int(expireTime["value"]) * 24 * 30 * 60
    elif expireTime["unit"] == "YEARLY" or expireTime["unit"] == "years":
        return int(expireTime["value"]) * 24 * 365 * 60
    else:
        return 0


# function converting time string to minutes format.
def convertStrToInt(time):
    hours, minutes = map(int, time.split(":"))
    total_minutes = hours * 60 + minutes
    return total_minutes


# function to give time difference
def time_difference(input_date):
    input_date = datetime.strptime(input_date, "%d:%m:%y %H:%M")
    current_time = datetime.now()  # change the now to time stamp.
    time_diff = input_date - current_time
    time_diff_minutes = int(time_diff.total_seconds() / 60)
    return time_diff_minutes


# funtion to convert recurrence time units into minutes
def recToUnitMinutes(schedule):
    expire = {
        "unit": schedule["recurrence"],
        "value": schedule["repeatInterval"]["every"],
    }
    return convertTimeMinutes(expire)


def projectionCount(data, givenTime):

    givenTimeMin = time_difference(givenTime)

    scheduleCount = {"projectionRun": {}, "Active": {}}

    protection_keys = ["arraySchedules", "onPremisesSchedules", "cloudStoreSchedules"]

    for protection_key in protection_keys:
        protection = data.get(protection_key, [])
        if protection_key == "arraySchedules":
            protectType = "SNAPSHOT"
            scheduleCount["projectionRun"]["SNAPSHOT"] = {}
        elif protection_key == "onPremisesSchedules":
            protectType = "BACKUP"
            scheduleCount["projectionRun"]["BACKUP"] = {}
        else:
            protectType = "CLOUD_BACKUP"
            scheduleCount["projectionRun"]["CLOUD_BACKUP"] = {}

        for schedule in protection:
            count = 0

            if givenTime and (givenTimeMin) < convertTimeMinutes(schedule["retainFor"]):
                print("giventime: ", givenTimeMin)
                print("retainfor: ", convertTimeMinutes(schedule["retainFor"]))
                print(
                    "backupFrequency: ", convertTimeMinutes(schedule["backupFrequency"])
                )

                count = math.ceil(
                    ((givenTimeMin) - convertStrToInt(schedule["StartAfter"]))
                    / convertTimeMinutes(schedule["backupFrequency"])
                )
            else:
                print("giventime: ", givenTimeMin)
                print("retainfor: ", convertTimeMinutes(schedule["retainFor"]))
                print(
                    "backupFrequency: ", convertTimeMinutes(schedule["backupFrequency"])
                )
                count = math.ceil(
                    ((givenTimeMin) - convertTimeMinutes(schedule["retainFor"]))
                    / convertTimeMinutes(schedule["backupFrequency"])
                )
            print(schedule["scheduleName"], " ", count)
            scheduleCount["projectionRun"][protectType][
                schedule["scheduleName"]
            ] = count

    for protection_key in protection_keys:
        protection = data.get(protection_key, [])
        if protection_key == "arraySchedules":
            protectType = "SNAPSHOT"
            scheduleCount["Active"]["SNAPSHOT"] = {}
        elif protection_key == "onPremisesSchedules":
            protectType = "BACKUP"
            scheduleCount["Active"]["BACKUP"] = {}
        else:
            protectType = "CLOUD_BACKUP"
            scheduleCount["Active"]["CLOUD_BACKUP"] = {}

        for schedule in protection:
            count = 0

            if givenTimeMin > 0:
                expireTimeMinutes = convertTimeMinutes(schedule["retainFor"])
                totalExpireMinutes = expireTimeMinutes
                # print(expireTimeMinutes)
                n = 1
                while True:
                    totalExpireMinutes = expireTimeMinutes * n
                    # print(schedule['name'], totalExpireMinutes)
                    # print('givenTime', givenTimeMin)
                    if totalExpireMinutes > givenTimeMin:
                        if n > 1:
                            n -= 1
                            totalExpireMinutes = expireTimeMinutes * n
                            break
                        else:
                            totalExpireMinutes = 0
                            break
                    n += 1
                # print('frequency minutes', recToUnitMinutes(schedule['schedule']))
                count = math.ceil(
                    (givenTimeMin - totalExpireMinutes)
                    / convertTimeMinutes(schedule["backupFrequency"])
                )
                scheduleCount["Active"][protectType][schedule["scheduleName"]] = count

    res = getValidTimestamps(
        data=data, given_time=givenTime, scheduleCount=scheduleCount
    )
    scheduleCount["CostAndSize"] = res
    # print(scheduleCount['CostAndSize'])
    print(json.dumps(scheduleCount, indent=4))
    return scheduleCount


if __name__ == "main":
    app.run(debug=True)
