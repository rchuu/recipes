from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


class Recipe:
    db = "recipes_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, under_30, date_made, user_id) VALUES (%(name)s,%(description)s,%(instruction)s,%(under_30)s,%(date_made)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM recipes
        WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """UPDATE recipes 
        SET name= %(name)s,
        description= %(description)s,
        instruction= %(instruction)s,
        date_made= %(date_made)s,
        under_30= %(under_30)s,
        updated_at= NOW()
        WHERE id= %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = """DELETE FROM recipes
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            is_valid = False
            flash("name is too short", "recipe")
        if len(recipe['instruction']) < 2:
            is_valid = False
            flash("instructions is too short", "recipe")
        if len(recipe['description']) < 2:
            is_valid = False
            flash("descriptions is too short", "recipe")
        if len(recipe['date_made']) == "":
            is_valid = False
            flash("missing a date", "recipe")
        if "under_30" not in recipe:
            is_valid = False
            flash("missing", "recipe")
        return is_valid
