from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
DB = "recipes_schema"

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes(name, description, instructions, created_at, time, user_id) VALUES (%(name)s,%(description)s, %(instructions)s, %(created_at)s,%(time)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        result = connectToMySQL(DB).query_db(query)
        recipes = []
        for rec in result:
            recipes.append(cls(rec))
        return recipes
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        print(result)
        print(result[0])
        return result[0]

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 4:
            flash("Please enter recipe name.", 'name')
            is_valid = False

        if len(recipe['description']) < 10:
            flash("Please enter a description for the recipe.", 'description')
            is_valid = False

        if len(recipe['instructions']) < 10:
            flash("Please give some instructions to help others.", 'instructions')
            is_valid = False

        return is_valid

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s,instructions=%(instructions)s, time=%(time)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)