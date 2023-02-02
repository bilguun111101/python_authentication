from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import mysql.connector

from passlib.hash import sha256_crypt

URL = "http://127.0.0.1:3000/users"

headers = {"Content-type": "application/json"}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")



@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password == confirm:
            json = { 'email': email, 'username': username, 'password': password }   
            r = requests.post(url = URL, json=json, headers=headers)
            
    return render_template('signup.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")
    return render_template("login.html")

@app.route("/content")
def content():
    return render_template("content.html")


@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logger out", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key="1.30/2:18intership_system_development"
    app.run(debug=True, port=5000)
    
    
      
# api-endpoint
# URL = "http://127.0.0.1:5000"
  
# # location given here
# location = "delhi technological university"
  
# # defining a params dict for the parameters to be sent to the API
# PARAMS = {'address':location}
  
# # sending get request and saving the response as response object
# r = requests.get(url = URL, params = PARAMS)
  
# # extracting data in json format
# data = r.json()
  
  
# # extracting latitude, longitude and formatted address 
# # of the first matching location
# latitude = data['results'][0]['geometry']['location']['lat']
# longitude = data['results'][0]['geometry']['location']['lng']
# formatted_address = data['results'][0]['formatted_address']
  
# # printing the output
# print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#       %(latitude, longitude,formatted_address))