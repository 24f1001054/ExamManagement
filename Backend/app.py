from model import *
from flask import Flask,flash,request,jsonify
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] ='sqlite:///exam.db'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
	return jsonify(message="Hello this is a homepage of webap")


@app.route("/api/register",methods=["POST","GET"])
def register():


	data = request.get_json()
	if not data:
		return jsonify({"error":"Invaid Request"})

	if request.method == "POST":
		username = data.get("username")
		email = data.get("email")
		password = data.get("password")
		role = data.get("role")

		if not username or not email or not password:
			return jsonify({"error": "Missing required fields"}), 400

		if role == "admin":
			return jsonify({"message": "Admin registration is not allowed"}), 403

		user = User.query.filter_by(username=username).first()
		if user:
			return jsonify({"message":f"{user.username} already found"})

		db.session.add(User(username=username,role=role,email=email,password=password))
		db.session.commit()
		return jsonify({"message":f"{username} Register sucessfully!🥳"})

@app.route("/api/login",methods=["POST","GET"])
def login():
	data = request.get_json()
	if not data:
		return jsonify({"error":"Invaid Request"})

	if request.method == "POST":
		email = data.get("email")
		password = data.get("password")
		

		if not email or not password:
			return jsonify({"error": "Missing required fields"}), 400
		
		user = User.query.filter_by(email=email).first()

		if user.email == email:
			if user.password == password:

				if user.role =="admin":
					return jsonify({"message":f"Admin {user.username}  login sucessfully !! 🥳"}),200
				
				if user.role == "examiner":
					if user.profile.status != "approved":
						return  jsonify({"message":f"Examiner {user.username} Wait for approval !! 🫷"}),200
					
					return jsonify({"message":f"Examiner {user.username}  login sucessfully !! 🥳"}),200

				
				return jsonify({"message":f" User {user.username} login sucessfully !!🥳"}),200
			
			return jsonify({"message":f"{email} password not correct "}),404

		return jsonify({"message":"User not exists, Go to Register page"})



@app.route("/api/add_course",methods=["GET","POST"])
def add_course():
	if request.method == "POST":
		data = request.get_json()
		if not data:
			return jsonify({"error":"Data not found"})
		
		c_code = data.get("code")
		c_name = data.get("name")
		description = data.get("description")
		status = data.get("status")

		course = Course.query.filter_by(c_code=c_code).first()

		if course:
			# if not c_code or not c_name or not description or not status:
			# 	return  jsonify({"error": "Missing required fields"}), 400
			return  jsonify({"Error": "Course already exist"}), 404
		new_course = Course(c_code=c_code,c_name=c_name,description=description,status=status)

		db.session.add(new_course)
		db.session.commit()
		return  jsonify({"Success": "Course created by Admin"}), 200
	
	
@app.route("/api/delete_course",methods=["GET","POST"])
def delete_course():
	if request.method == "POST":
		data = request.get_json()
		if not data:
			return jsonify({"error":"Data not found"})
		
		c_code = data.get("code")
		

		course = Course.query.filter_by(c_code=c_code).first()

		if not course:
			return  jsonify({"Not Found": "Course not exists !!"}), 400
		

		db.session.delete(course)
		db.session.commit()
		return  jsonify({"Success": "Course Deleted by Admin"}), 200
	
		# return  jsonify({"Error": "Course already exist"}), 404



@app.route("/api/create_exam",methods=["POST","GET"])
def create_examination():
	if request.method == "POST":
		data = request.get_json()
		

		if not data:
			return jsonify({"error":"data not nor given"}),404

		course_id = data.get("course_id")
		exam_name = data.get("exam_name")
		exam_type = data.get("exam_type")
		duration = data.get("duration")
		max_marks = data.get("max_mark")

		slot_start = data.get("slot_start")
		slot_start = datetime.strptime(slot_start,"%H-%M").time() # changing datatype

		slot_end = data.get("slot_end")
		slot_end = datetime.strptime(slot_end,"%H-%M").time() # changing datatype

		booking_start = data.get("booking_start")
		booking_start = datetime.strptime(booking_start,"%Y-%m-%d").date() # changing datatype

		booking_end = data.get("booking_end")
		booking_end = datetime.strptime(booking_end,"%Y-%m-%d").date() # changing datatype

		status = data.get("status")

		course = Course.query.filter_by(id=course_id).first()
		if course:
			exists_exam = Examination.query.filter_by(ex_name=exam_name,course_id=course_id).first()

			if exists_exam:
				return jsonify({"message":"Examination already registered"}),404

			if slot_end <= slot_start:
				return jsonify({"message":"Invaild Slot time"}),404
				
			if booking_end <= booking_start:
				return jsonify({"message":"Invaild Booking start and end timing adjust it"}),404


			exam = Examination(
				course_id = course_id,ex_name=exam_name,ex_type=exam_type,duration=duration,max_mark=max_marks,slot_start=slot_start,slot_end=slot_end,booking_end=booking_end,booking_start=booking_start,status=status
			)
			db.session.add(exam)
			db.session.commit()
			return jsonify({
				"message":"Examination created successfully !! ",
				"exam_id":exam.id
			}),200
		
		return jsonify({"message":"Course not exists"}),404

		

		





		
		

		
###--------------Admin features ----------###









#--------student features ---------#

#@app.route("/api/students/")
		

			

























	
if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		print(db.engine.url.database)

		admin = User.query.filter_by(role='admin').first()

		if not admin:
			user = User(email="admin1@gmail.com",password='123',username='admin1',role='admin')
			
			db.session.add(user)
			db.session.commit()
		print("Admin already exists please Login!!")

	app.run(debug=True,use_reloader=False)
