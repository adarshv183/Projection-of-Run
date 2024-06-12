import json
from datetime import datetime, timedelta
from backend.PolicyCostSize import projectCost

# with open("C:/Users/USER/OneDrive/Desktop/projectionCount/Projection-of-RPC-and-AC/json_files/new_json2.json") as data_file:
#     req_payload = json.load(data_file)

# with open("../json_files/new_json.json") as data_file:
#     req_payload = json.load(data_file)

# scheduleCount = {
#     "projectionRun": {
#         "SNAPSHOT": {"Array_Snapshot_1": 40, "Array_Snapshot_2": 7},
#         "BACKUP": {
#             "On-Premises_Protection_Store_3": 7,
#             "On-Premises_Protection_Store_4": 1,
#         },
#         "CLOUD_BACKUP": {
#             "HPE_Cloud_Protection_Store_5": 1,
#             "HPE_Cloud_Protection_Store_6": 1,
#         },
#     },
#     "Active": {
#         "SNAPSHOT": {"Array_Snapshot_1": 4, "Array_Snapshot_2": 7},
#         "BACKUP": {
#             "On-Premises_Protection_Store_4": 7,
#             "On-Premises_Protection_Store_7": 1,
#         },
#         "CLOUD_BACKUP": {
#             "HPE_Cloud_Protection_Store_5": 1,
#             "HPE_Cloud_Protection_Store_6": 1,
#         },
#     },
# }


def convert_to_minutes(time, recurrence):
    if recurrence == "HOURLY" or recurrence == "hours":
        return time * 60
    elif recurrence == "DAILY" or recurrence == "days":
        return time * 24 * 60
    elif recurrence == "WEEKLY" or recurrence == "weeks":
        return time * 24 * 7 * 60
    elif (
        recurrence == "MONTHLY" or recurrence == "months"
    ):  # assuming avg 30 days per month
        return time * 24 * 30 * 60
    elif recurrence == "YEARLY" or recurrence == "years":
        return time * 24 * 365 * 60
    else:
        return 0


def recentTimestamp(start_time, end_time, interval_minutes, target_time):
    # Convert strings to datetime objects

    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")
    target_time = datetime.strptime(target_time, "%d:%m:%y %H:%M")

    # Determine the start and end time for the task on the target date
    task_start_time = start_time
    task_end_time = target_time.replace(
        hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0
    )

    last_task_time = None
    if task_start_time <= target_time:
        last_task_time = task_start_time

    # print(
    #     f"{type(task_start_time)},{type(task_end_time)},{type(target_time)}, {type(interval_minutes)}"
    # )

    while task_start_time <= task_end_time:
        task_start_time += timedelta(minutes=interval_minutes)
        if task_start_time <= target_time:
            last_task_time = task_start_time
        # print(f"{task_start_time},{task_end_time},{target_time}")

    # print(last_task_time)
    return last_task_time


"""New JSON FORMAT"""


def getTimeStampsForEachCount(res, scheduleCount):
    # print(scheduleCount)
    for obj in res:
        # print(obj)
        print("----")
        # identify the active counts from schdeule cost
        absolute_copies = (
            scheduleCount.get("Active").get(obj.get("type")).get((obj.get("name")))
        )
        # print(absolute_copies)
        back_track_time = obj.get("timestamp")
        timestamps = []
        print(scheduleCount.get("Active").get(obj.get("type")).get((obj.get("name"))))
        for i in range(0, absolute_copies):
            timestamps.append(back_track_time.strftime("%Y-%m-%d %H:%M:%S"))
            back_track_time -= timedelta(minutes=obj.get("interval"))
            i += 1
        obj["timestamps"] = timestamps
        # print(obj)
        print("----")
    print(json.dumps(res, indent=4, default=str))
    information = {
        "SNAPSHOT": {"full_backup": 50, "cost": 20, "c_ratio": 0.04},
        "BACKUP": {"full_backup": 55, "cost": 40, "c_ratio": 0.1},
        "CLOUD_BACKUP": {"full_backup": 80, "cost": 60, "c_ratio": 0.1},
    }
    response = projectCost(res, information=information)
    return response

"""Old JSON FORMAT"""
# def getValidTimestamps(data, given_time, scheduleCount):
#     # print(scheduleCount)
#     print("-----------------------")
#     res = []
#     start_date = data.get("createdAt").split("T")[0]
#     for protection in data["protections"]:
#         for schedule in protection["schedules"]:
#             name = schedule.get("name")
#             repeat_interval = convert_to_minutes(
#                 schedule.get("schedule").get("repeatInterval").get("every"),
#                 schedule.get("schedule").get("recurrence"),
#             )
#             try:
#                 start_window = start_date + " " + schedule["schedule"]["startTime"]
#                 end_window = "23:59"
#             except KeyError:
#                 start_window = (
#                     start_date
#                     + " "
#                     + schedule["schedule"]["activeTime"]["activeFromTime"]
#                 )
#                 end_window = schedule["schedule"]["activeTime"]["activeUntilTime"]

#             # print(name)
#             timestamp = recentTimestamp(
#                 start_window, end_window, repeat_interval, given_time
#             )

#             # print(timestamp)

#             res.append(
#                 {
#                     "name": name,
#                     "type": protection.get("type"),
#                     "timestamp": timestamp,
#                     "interval": repeat_interval,
#                 }
#             )
#     getTimeStampsForEachCount(res, scheduleCount)
#     return res


def getValidTimestamps(data, given_time, scheduleCount):
    res = []
    start_date = data.get("createdAt").split("T")[0]
    for protection in [
        "arraySchedules",
        "onPremisesSchedules",
        "cloudStoreSchedules",
    ]:
        for schedule in data[protection]:
            id = schedule.get("scheduleId")
            repeat_interval = convert_to_minutes(
                int(schedule.get("backupFrequency").get("value")),
                schedule.get("backupFrequency").get("unit"),
            )
            start_window = start_date + " " + schedule.get("StartAfter")
            end_window = "23:59"
            # except TypeError:
            #     start_window = start_date + " " + schedule.get("timeRangeStart")
            #     end_window = schedule.get("timeRangeEnd")

            if protection == "arraySchedules":
                protectType = "SNAPSHOT"
            elif protection == "onPremisesSchedules":
                protectType = "BACKUP"
            else:
                protectType = "CLOUD_BACKUP"

            # print(id)
            timestamp = recentTimestamp(
                start_window, end_window, repeat_interval, given_time
            )

            res.append(
                {
                    "id": id,
                    "name": schedule.get("scheduleName"),
                    "type": protectType,
                    "timestamp": timestamp,
                    "interval": repeat_interval,
                }
            )
    print(json.dumps(res, indent=4, default=str))
    response = getTimeStampsForEachCount(res, scheduleCount=scheduleCount)
    return response


if __name__ == "__main__":
    res = getValidTimestamps(req_payload, "25:06:24 23:25", scheduleCount=scheduleCount)
    print(json.dumps(res, indent=4, default=str))
# ...

# if _name_ == "_main_":
#     res = getValidTimestamps(req_payload, "2024-03-25 11:00")
#     print(json.dumps(res, indent=4, default=str))
