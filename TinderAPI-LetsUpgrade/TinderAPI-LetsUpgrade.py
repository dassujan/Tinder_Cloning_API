import firebase_admin
from firebase_admin import auth, firestore, storage, credentials
from flask import abort, jsonify, request, redirect
import json
import requests

app = flask.Flask(__name__)

cred = credentials.Certificate(
    "tinderapi-letsupgrade-9d8d7-firebase-adminsdk-ehaxm-53c18064e5.json")
firebase_app firebase_admin.initialize_app(cred)
store = firestore.client()


@app.route('/login', methods=['POST'])
def login():
	data = requests.get_json(force=True)
	emailOfUser = data.get("email")
	uid = ""
	message = ""
	try:
		user = auth.get_user_by_email(emailOfUser)
		message = "Succesfully Got The new user"
		uid = user.uid
	except:
		messge = "User not there in firebase"
    return jsonify({"Response": 200, "uid": uid, "message" : message })

@app.route('/login', methods=['POST'])
def signUp(emailOfUser, passwordOfUser):
      uid = ""
  message = ""
  try:
    user = auth.create_user(
        email = emailOfUser,
        email_verified = False,
        password = passwordOfUser)
    message = "Successsfully Created New User"
    uid = user.uid
  except:   
    message = "User Already There"

  return jsonify{"uid": uid, "message" : message, "Response": 200}

@app.route('/abc', methods=['GET'])
def abc():
    data = request.get_json(force=True)
    print("Hi Guys")
    return ({"Response": 200, "Message":"It works"})

@app.route('/userUpdate', methods=['POST'])
def userUpdate():
    dit = requests.get_json(force=True)
    
    uid = dit.get['uid']
    dit_user_details= {}

    dit_user_details["name"] = dit["name"]
    dit_user_details["email"] = dit["email"]
    dit_user_details["number"] = dit["number"]
    dit_user_details["image"] = dit["image"]
    dit_user_details["desp"] = dit["desp"]
    dit_user_details["dob"] = dit["dob"]
    dit_user_details["gender"] = dit["gender"]
    dit_user_details["passion"] = dit["passion"]
    dit_user_details["job"] = dit["job"]
    dit_user_details["company"] = dit["company"]
    dit_user_details["location"] = dit["location"]

    dit_user_details["createdAt"] = firestore.SERVER_TIMESTAMP
    store.collection("users").document(uid).set(dit_user_details)

    message = "User Data Updated"

    # emailOfUser = data.get("email")
    # passwordOfUser = data.get("password")
    # uid = ""
    # message = ""
    # try:
    #     user = auth.create_user(
    #         email=emailOfUser,
    #         email_verified=False,
    #         password=passwordOfUser)
    #     message = "Successfully created new user"
    #     uid = user.uid
    # except:
    #     message = "User already there"

    return {"uid": uid, "message": message, "Response": 200}


    # return jsonify({"Response": 200})


if __name__ == '__main__':
    app.run(host='0.0.0.0.', port=5001, debug=False)