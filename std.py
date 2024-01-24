from flask import request,Flask,jsonify
from flask_basicauth import BasicAuth
app = Flask(__name__) 

app.config['BASIC_AUTH_USERNAME']='username'
app.config['BASIC_AUTH_PASSWORD']='password'
basic_auth = BasicAuth(app)

std=[
    {"id":1,"name":"James","major":"T12","gpa":"3.00"},
    {"id":2,"name":"Mint","major":"T12","gpa":"3.00"},
    {"id":3,"name":"Pluem","major":"T12","gpa":"3.50"},
    {"id":4,"name":"Terk","major":"T12","gpa":"4.00"},
    {"id":5,"name":"xxxxx","major":"T12","gpa":"0.00"}
]
@app.route("/")
def Greet():
    return "<p>Welcome to Student Management Systems</p>"

@app.route("/students",methods=["GET"])
@basic_auth.required
def get_all_students():
    return jsonify({"students":std})

@app.route("/students/<int:student_id>",methods=["GET"])
@basic_auth.required
def get_book(student_id):
    student=next( (b for b in std if b["id"]==student_id),None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error":"Student not found"}),404

@app.route("/students",methods=["POST"])
@basic_auth.required
def create_student():
    data = request.get_json()
    new_student ={
        "id":len(std)+1,
        "name":data["name"],
        "major":data["major"],
        "gpa":data["gpa"]
    }
    std.append(new_student)
    return jsonify(new_student),200

@app.route("/students/<int:student_id>",methods=["PUT"])
@basic_auth.required
def update_student(student_id):
    student = next((b for b in std if b["id"] == student_id),None)
    if student:
        data = request.get_json()
        student.update(data)
        return jsonify(student),200
    else:
        return jsonify({"error" : "student not found"}),404
    

@app.route("/students/<int:student_id>",methods=["DELETE"])
@basic_auth.required
def delete_student(student_id):
    student = next((b for b in std if b["id"]==student_id),None)
    if student:
        std.remove(student)
        return jsonify({"message":"Student deleted successfully"}),200
    else:
        return jsonify({"error":"Student not found"}),404
    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)

