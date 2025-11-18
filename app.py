from flask import Flask, request, jsonify

app = Flask(__name__)

# -------- In-Memory User Storage --------
users = {}
current_id = 1


# -------- Helper Function --------
def validate_user_payload(data):
    if not data:
        return "Request must contain JSON data.", False
    if "name" not in data or "email" not in data:
        return "Fields 'name' and 'email' are required.", False
    return "", True


# ----------- ROUTES -----------

# Health check
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "User API is running successfully"}), 200


# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"total": len(users), "users": users}), 200


# GET single user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id]), 200


# CREATE user
@app.route("/users", methods=["POST"])
def create_user():
    global current_id
    data = request.json

    # Validate JSON payload
    msg, valid = validate_user_payload(data)
    if not valid:
        return jsonify({"error": msg}), 400

    user = {
        "id": current_id,
        "name": data["name"],
        "email": data["email"]
    }

    users[current_id] = user
    current_id += 1

    return jsonify({"message": "User created successfully", "user": user}), 201


# UPDATE user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    msg, valid = validate_user_payload(data)
    if not valid:
        return jsonify({"error": msg}), 400

    users[user_id]["name"] = data["name"]
    users[user_id]["email"] = data["email"]

    return jsonify({"message": "User updated", "user": users[user_id]}), 200


# DELETE user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    deleted_user = users.pop(user_id)
    return jsonify({"message": "User deleted", "deleted": deleted_user}), 200


if __name__ == "__main__":
    app.run(debug=True)
