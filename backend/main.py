# CRUD
#Create
#Read
#Update
#Delete
from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    #handle get req
    contacts = Contact.query.all()
    #iterates over list (contacts) and returns new list
    #lambda - one line function
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name, and an email."}),
            400
        )

    #create contact
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        #stage new record
        db.session.add(new_contact)
        #write to db
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    #we're good
    return jsonify({"message": "User created!"}), 201

@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
#/update_contact/{id}
def update_contact(user_id):
    #get contact by user_id
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User does not exist."}), 404

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User " + str(user_id) + " updated"}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    #get contact by user_id
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User does not exist."}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User " + str(user_id) + " deleted"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all() #spins up DB and all models

    app.run(debug=True)