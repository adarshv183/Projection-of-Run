import json

# with open(
#     "D:/Adhi/BMS/HPE-CTY/Projection-of-Run/json_files/new_json2.json", "r"
# ) as data_file:
#     data = json.load(data_file)


# function for converting the time to lowest possible unit - hours
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


# Class TreeNode
class TreeNode:

    def __init__(self, id, schedule_type, start_time, interval):
        self.id = id
        self.type = schedule_type
        self.startTime = start_time
        self.interval = interval
        self.children = []

    def add_child(self, child):
        self.children.append(child)


# creation of tree
def build_tree(data):
    protections = ["arraySchedules", "onPremisesSchedules", "cloudStoreSchedules"]
    root = TreeNode("root", "root", "root", "root")
    schedule_map = {}

    for protection in protections:
        schedule_type = protection
        if schedule_type == "arraySchedules":
            schedule_type = "SNAPSHOT"
        elif protection == "onPremisesSchedules":
            schedule_type = "BACKUP"
        else:
            schedule_type = "CLOUD_BACKUP"
        for schedule in data[protection]:
            # schedule_id = int(schedule["scheduleId"]["$numberInt"])
            schedule_id = int(schedule["scheduleId"])
            startTime = data["createdAt"].split("T")[0] + " " + schedule["StartAfter"]
            interval = convert_to_minutes(
                int(schedule.get("backupFrequency").get("value")),
                schedule.get("backupFrequency").get("unit"),
            )

            schedule_map[schedule_id] = schedule

            if schedule_type == "SNAPSHOT":
                root.add_child(
                    TreeNode(schedule_id, schedule_type, startTime, interval)
                )

            else:
                # parent_id = int(schedule.get("sourceScheduleId").get("$numberInt"))
                parent_id = int(schedule.get("sourceScheduleId"))
                if parent_id in schedule_map:
                    parent_node = find_node(root, parent_id)
                    if parent_node:
                        parent_node.add_child(
                            TreeNode(schedule_id, schedule_type, startTime, interval)
                        )
                else:
                    print(
                        f"Parent schedule with id {parent_id} not found for schedule {schedule_id}."
                    )

    return root


def find_node(root, target_id):
    if root.id == target_id:
        return root
    for child in root.children:
        node = find_node(child, target_id)
        if node:
            return node
    return None


# utility function
def tree_to_dict(node):
    result = {
        "id": str(node.id),
        "type": str(node.type),
        "startTime": str(node.startTime),
        "interval": str(node.interval),
    }
    if node.children:
        result["children"] = [tree_to_dict(child) for child in node.children]
    return result


lis = [
    {
        "Id": "parent",
        "Role": "root",
    }
]


def tree_to_list_format(node):
    if node.children:
        for child in node.children:
            lis.append(
                {
                    "Id": int(child.id),
                    "Role": str(child.type) + " " + str(child.id),
                    "Team": "parent" if (str(node.id) == "root") else str(node.id),
                }
            )
            print(lis)
            tree_to_list_format(child)
    return lis


# search for possible paths
def find_all_paths(root):
    paths = []
    current_path = []

    def dfs(node):
        if not node:
            return
        current_path.append(
            {
                "id": node.id,
                "startTime": node.startTime,
                "interval": node.interval,
                "type": node.type,
            }
        )
        if not node.children:
            paths.append(list(current_path))
        else:
            for child in node.children:
                dfs(child)
        current_path.pop()

    dfs(root)
    return paths


# if __name__ == "__main__":
#     root = build_tree(data)
#     print(json.dumps(tree_to_dict(root), indent=4, default=4))
