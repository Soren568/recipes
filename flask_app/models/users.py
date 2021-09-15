from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DB = "recipes_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def full_name():
        return 
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s,%(password)s);"
        return connectToMySQL(DB).query_db(query, data)

# ================================= VALIDATE =================================
    @staticmethod
    def validate_user(user):
        is_valid = True
        
        # Name check
        if len(user['first_name']) < 1 or len(user['last_name']) < 1:
            flash("Please enter your name.", 'name')
            is_valid = False

        # email check
        e_results = User.get_by({"email":user['email']})
        print(e_results)
        if e_results:
            flash("Email already registered.", "email")
            print("test")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email input.", "email")
            is_valid = False

        # Password confirmation check
        if not PW_REGEX.match(user['password']):
            flash("Password does not meet criteria. Please follow given instructions.", "pw_length")
            is_valid = False
        if user['password'] != user['pw_confirm']:
            flash("Passwords did not match.", "pw_confirm")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, user):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DB).query_db(query,user)
        if results:
            return cls(results[0])
# ==============================================================================

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        print("test", data)
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])

    @classmethod
    def get_by(cls, user):
        where = " AND ".join(f"{key} = %({key})s" for key in user)
        query = "SELECT * FROM users WHERE " + where
        result = connectToMySQL(DB).query_db(query, user)
        if result:
            return cls(result[0])