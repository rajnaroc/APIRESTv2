from flask import Flask,jsonify, request
from flask.cli import load_dotenv
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL
from bson import ObjectId
import os

load_dotenv()

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb+srv://rajnaroc:12345@cluster0.r5gm8.mongodb.net/users"

app.config["MYSQL_HOST"]="b68fttvw3vrzskmx10ds-mysql.services.clever-cloud.com"
app.config["MYSQL_USER"]="usrftefhmotkb5ao"
app.config["MYSQL_PASSWORD"]="KRYZo60SCwVTgcYoijxx"
app.config["MYSQL_DB"]="b68fttvw3vrzskmx10ds"

mysql = MySQL(app)

mongo = PyMongo(app)


@app.route('/addmongo', methods=["POST"])
def addmongo():
    nombre = request.json["nombre"]
    color = request.json["color"]
    edad = request.json["edad"]
    numero = request.json["numero"]

    if nombre and color and edad and numero:
        id = mongo.db.users.insert_one({
            "nombre": nombre,
            "color": color,
            "edad" : edad,
            "numero": numero
            })
        response = {
            "id": str(id.inserted_id),
            "nombre" : nombre,
            "color" : color,
            "edad" : edad,
            "numero": numero
        }

        return jsonify(response),200
    
@app.route('/usersmongo', methods=["GET"])
def usersmongo():
    users = mongo.db.users.find()
    return jsonify(users)

@app.route('/usermongo/<id>', methods=["GET"])
def usermongo(id):
    users = mongo.db.users.find({"_id": ObjectId(id)})
    if users:
        return jsonify({users})
    
@app.route('/deletemongo/<id>', methods=["DELETE"])
def deletemongo(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})
    
    return jsonify({"message" : "elimando el" + id})

@app.route('/update/<id>', methods=["PUT"])
def updatemongo(id):
    nombre = request.json["nombre"]
    color = request.json["color"]
    edad = request.json["edad"]
    numero = request.json["numero"]
    
    user = mongo.db.users.update_one({"_id": ObjectId(id)},{"$set":{
        "nombre": nombre,
        "color": color,
        "edad" : edad,
        "numero" : numero
    }})
    
    return jsonify({user})

@app.route('/addsql', methods=["POST"])
def addmysql():
    nombre = request.json["nombre"]
    color = request.json["color"]
    edad = request.json["edad"]
    numero = request.json["numero"]
    if nombre and color and edad and numero:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users VALUES (NULL,%s,%s,%s,%s)",(nombre,color,edad,numero))
        mysql.connection.commit()
        return jsonify({"usuario": {"nombre": nombre,"color":color, "edad": edad, "numero": numero }})
    return jsonify({"message": "error al insertar datos"})

@app.route('/userssql', methods=["GET"])
def userssql():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    datos = cur.fetchall()

    return jsonify(datos)


@app.route('/usersql/<id>', methods=["GET"])
def user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s",(id,))
    datos = cur.fetchall()

    return jsonify(datos)

@app.route('/deletesql/<id>',  methods=["DELETE"])
def deletesql(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s",(id,))
    mysql.connection.commit()

    return jsonify({"message": "Elimando El " + id})

@app.route('/updatesql/<id>',methods=["PUT"])
def updatesql(id):
    nombre = request.json["nombre"]
    color = request.json["color"]
    edad = request.json["edad"]
    numero = request.json["numero"]
    if nombre and color and edad and numero:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nombre = %s,color = %s,edad = %s,numero = %s WHERE id = %s",(nombre,color,edad,numero,id))
        mysql.connection.commit()

        return jsonify({"message" : {"nombre":nombre,"color":color,"edad":edad,"numero":numero}})


def error_404(error):
    return " 404 Resource not Found"


if __name__ == "__main__":
    app.register_error_handler(404,error_404)
    app.run(debug=True,host="0.0.0.0")