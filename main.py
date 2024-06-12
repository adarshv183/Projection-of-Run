import json
from flask import Flask, jsonify, request
from datetime import datetime
from flask_cors import CORS
import pymongo
from backend.projectionCountUpdated import projectionCount
import backend.policyTree as PolicyTree
import backend.getOverlaps as GetOverlaps

app = Flask(__name__)
CORS(app)

# conn_str = "mongodb+srv://sanketemalasge2:hpe123@cluster0.0iph2l9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

conn_str = "mongodb+srv://saiis21:hpe2444@cluster0.vaxb7qe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = pymongo.MongoClient(conn_str)
except Exception as e:
    print("error: ", e)

db = client["HPE"]
collection = db["Policy Json"]


class APIError(Exception):
    code = 400
    description = "Bad Request  - custom"
    pass


def compare(start, query):
    query = datetime.strptime(query, "%Y-%m-%d %H:%M")
    start = datetime.strptime(
        start,
        "%Y-%m-%dT%H:%M:%S.%fZ",
    )
    if start > query:
        raise APIError("query date and time is before created time of the policy.")


@app.errorhandler(APIError)
def handle_exception(err):
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]

    app.logger.error(f"{err.description}: {response.get('message')}")
    return jsonify(response), err.code


# with open("json_files/new_json2.json", "r") as data_file:
#     data = json.load(data_file)


@app.route("/get_overlaps", methods=["POST"])
def get_overlaps():
    # end_time = request.args.get("end_time")
    givenTime = request.get_json()
    print("givenTime is: ", givenTime)
    try:
        jsonData = collection.find_one({"policyName": givenTime["policyName"]})
        # print(jsonData)
    except MongoError as e:
        print(e)
    # compare(data.get("createdAt"), end_time)
    root = PolicyTree.build_tree(jsonData)
    paths = PolicyTree.find_all_paths(root)
    occurrences = GetOverlaps.get_res(paths, givenTime["givenTime"])
    return jsonify(occurrences)


@app.route("/get_policy_tree", methods=["POST"])
def get_policy_tree():
    req = request.get_json()
    print(req)
    try:
        jsonData = collection.find_one({"policyName": req["data"]["policy"]})
        # print(jsonData)
    except MongoError as e:
        print(e)
    print(json.dumps(jsonData, indent=4, default=str))
    return jsonify(PolicyTree.tree_to_list_format(PolicyTree.build_tree(jsonData)))


# @app.route("/givenTime", methods=["POST"])
# def projection_count():
#     print(request.get_json())
#     givenTime = request.get_json()

#     print('givenTime is: ', givenTime)
#     # jsonData = collection.find_one({"policyName":givenTime['policyName']})
#     # print(jsonData)
#     scheduleCount = projectionCount(data, givenTime=givenTime['givenTime'])
#     return jsonify(scheduleCount)


@app.route("/givenTime", methods=["POST"])
def projection_count():
    # print(request.get_json())
    givenTime = request.get_json()

    print("givenTime is: ", givenTime)
    try:
        jsonData = collection.find_one({"policyName": givenTime["policyName"]})
        # print(jsonData)
    except MongoError as e:
        print(e)
    scheduleCount = projectionCount(jsonData, givenTime=givenTime["givenTime"])
    return jsonify(scheduleCount)


@app.route("/jsondata", methods=["POST"])
def jsondata():
    data = request.json
    print("Received data:", data)
    return jsonify({"message": "Total object received successfully"}), 200


@app.route("/database", methods=["POST"])
def database():
    try:
        data = request.json

        policy_name = data.get("policyName")

        if policy_name:
            # Check if a policy with the same name already exists
            existing_policy = collection.find_one({"policyName": policy_name})
            if existing_policy:
                print("name already exists")
                return jsonify({"error": "Policy name already exists"}), 400

            # Insert the data into the MongoDB collection
            result = collection.insert_one(data)
            # Return a success message with the inserted ID
            return (
                jsonify(
                    {
                        "message": "Data inserted successfully",
                        "id": str(result.inserted_id),
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Policy name is required"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
