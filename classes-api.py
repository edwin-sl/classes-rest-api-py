from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory database (for demonstration purposes)
# In a real application, you would use a proper database
classes = [
    {
        "id": 1,
        "name": "Mathematics 101",
        "teacher": "Dr. Smith",
        "schedule": "Mon/Wed 9:00 AM",
        "students": 25,
        "room": "A101"
    },
    {
        "id": 2,
        "name": "Physics 101",
        "teacher": "Prof. Johnson",
        "schedule": "Tue/Thu 10:00 AM",
        "students": 20,
        "room": "B202"
    }
]

# Helper function to find a class by ID
def find_class(class_id):
    return next((c for c in classes if c["id"] == class_id), None)

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get all classes"""
    return jsonify(classes)

@app.route('/api/classes/<int:class_id>', methods=['GET'])
def get_class(class_id):
    """Get a specific class by ID"""
    class_item = find_class(class_id)
    if class_item is None:
        return jsonify({"error": "Class not found"}), 404
    return jsonify(class_item)

@app.route('/api/classes', methods=['POST'])
def create_class():
    """Create a new class"""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    
    # Validate required fields
    required_fields = ["name", "teacher", "schedule", "students", "room"]
    if not all(field in data for field in required_fields):
        return jsonify({
            "error": f"Missing required fields. Required fields are: {', '.join(required_fields)}"
        }), 400

    # Generate new ID (in a real application, this would be handled by the database)
    new_id = max(c["id"] for c in classes) + 1 if classes else 1
    
    new_class = {
        "id": new_id,
        "name": data["name"],
        "teacher": data["teacher"],
        "schedule": data["schedule"],
        "students": data["students"],
        "room": data["room"]
    }
    
    classes.append(new_class)
    return jsonify(new_class), 201

@app.route('/api/classes/<int:class_id>', methods=['PUT'])
def update_class(class_id):
    """Update an existing class"""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    class_item = find_class(class_id)
    if class_item is None:
        return jsonify({"error": "Class not found"}), 404

    data = request.get_json()
    
    # Update fields
    class_item.update({
        "name": data.get("name", class_item["name"]),
        "teacher": data.get("teacher", class_item["teacher"]),
        "schedule": data.get("schedule", class_item["schedule"]),
        "students": data.get("students", class_item["students"]),
        "room": data.get("room", class_item["room"])
    })
    
    return jsonify(class_item)

@app.route('/api/classes/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    """Delete a class"""
    class_item = find_class(class_id)
    if class_item is None:
        return jsonify({"error": "Class not found"}), 404
    
    classes.remove(class_item)
    return jsonify({"message": "Class deleted successfully"}), 200

@app.route('/api/classes/search', methods=['GET'])
def search_classes():
    """Search classes by teacher or room"""
    teacher = request.args.get('teacher')
    room = request.args.get('room')
    
    results = classes
    
    if teacher:
        results = [c for c in results if teacher.lower() in c["teacher"].lower()]
    if room:
        results = [c for c in results if room.lower() in c["room"].lower()]
        
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
