from collections import OrderedDict
import json
from math import gcd
from datetime import datetime, timedelta
import backend.policyTree as PolicyTree


def find_recent_source(path, endTime):
    # list to stores all the possible occurences for given path
    occurrences = []
    time_format = "%Y-%m-%d %H:%M"
    times = []
    for p in path:
        # initial time for all the schedules. can be modified with desired initial starttime
        times.append(datetime.strptime(p.get("startTime"), time_format))
    endTime = datetime.strptime(endTime, "%d:%m:%y %H:%M")
    print(f"end time : {endTime.strftime(time_format)}")
    while all(time < endTime for time in times):
        min_time = min(times)
        min_indices = [index for index, value in enumerate(times) if value == min_time]
        # print(f"times : {times}")
        # print(f"min_indices : {min_indices}")
        for idx in min_indices:
            if path[idx].get("type") != "SNAPSHOT":  # not snapshot
                # print the link present, either cloud backup or on-prem
                source_time = times[idx - 1] - timedelta(
                    minutes=path[idx - 1].get("interval")
                )
                print(
                    f"source : {source_time.strftime(time_format)} [{path[idx-1]['id']}] -> current : {times[idx].strftime(time_format)} [{path[idx]['id']}]"
                )
                occurrences.append(
                    {
                        "id": path[idx]["id"],
                        "time": times[idx].strftime(time_format),
                        "source_id": path[idx - 1]["id"],
                        "source_time": source_time.strftime(time_format),
                    }
                )
                times[idx] += timedelta(minutes=path[idx].get("interval"))
            else:
                print(
                    f"current : {times[idx].strftime(time_format)} [{path[idx]['id']}]"
                )
                occurrences.append(
                    {
                        "id": path[idx]["id"],
                        "time": times[idx].strftime(time_format),
                        "source_id": "None",
                        "source_time": "None",
                    }
                )
                times[idx] += timedelta(hours=path[idx].get("interval"))

    return occurrences


# for all the valid paths we are going to find the overlaps
def get_res(paths, endTime):
    res = []
    for path in paths:
        print(path[1:])
        res.append(
            {
                "schedules_involved": path[1:],
                "occurrences": find_recent_source(path[1:], endTime),
            }
        )
    return res
