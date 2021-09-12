from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/recipe/create')
def create_recipe_page():
    return render_template("add.html", active_user = User.get_by_id({"id":session['user_id']}))

@app.route('/recipe/save', methods=["POST"])
def save_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')
    Recipe.save(request.form)
    flash(f"{request.form['name']} added to recipes list! Thanks for your contribution to ending world hunger.", "recipe_added")
    return redirect('/dashboard')

@app.route('/recipe/info/<int:id>')
def show_recipe(id):
    return render_template("recipe.html", recipe = Recipe.get_by_id({"id":id}))

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    return render_template("edit.html", recipe = Recipe.get_by_id({"id":id}))

@app.route('/recipe/update', methods=["POST"])
def update_recipe():
    Recipe.update(request.form)
    flash("Recipe updated!", "recipe_update")
    return redirect('/dashboard')

@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete({"id": id})
    flash("Recipe deleted!", "recipe_delete")
    return redirect('/dashboard')

@app.route('/dashboard')
def recipe_dashboard():
    return render_template("dashboard.html", active_user = User.get_by_id({"id":session['user_id']}), recipes = Recipe.get_all())