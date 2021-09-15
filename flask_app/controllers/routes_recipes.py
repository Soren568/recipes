from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
from datetime import date, datetime
bcrypt=Bcrypt(app)

@app.route('/recipe/create')
def create_recipe_page():
    # Validates that session id is correct
    if not User.get_by({"id":session['user_id']}):
        flash("Something went wrong with the id.", "bad_id")
        return redirect('/')
    if not session:
        return redirect('/')
    return render_template("add.html", active_user = User.get_by_id({"id":session['user_id']}))
# custom decorator to reduce active_user

@app.route('/recipe/save', methods=["POST"])
def save_recipe():
    # Ensures page cannot be accessed w/o session (created on login)
    if not session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')
    Recipe.save(request.form)
    flash(f"{request.form['name']} added to recipes list! Thanks for your contribution to ending world hunger.", "recipe_added")
    return redirect('/dashboard')

@app.route('/recipe/info/<int:id>')
def show_recipe(id):
    if not session:
        return redirect('/')
    return render_template("recipe.html", recipe = Recipe.get_by_id({"id":id}))

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    if not session:
        return redirect('/')
    recipe = Recipe.get_by_id({"id":id})
    print(session['user_id'], ",",recipe.user_id)
    if session['user_id'] != recipe.user_id:
        flash("Your not allowed in there.", "bad_edit")
        return redirect('/dashboard')
    return render_template("edit.html", recipe = recipe)

@app.route('/recipe/update/<int:id>', methods=["POST", "GET"])
def update_recipe(id):
    if not session:
        return redirect('/')
    # check to see if user editing is the logged in user - all done outside of through the browser
    recipe = Recipe.get_by_id({"id":id})
    if session['user_id'] != recipe.user_id:
        flash("Your not allowed in there.", "bad_edit")
        return redirect('/dashboard')
    if datetime.strptime(request.form['made_on'], "%Y-%m-%d") > datetime.now():
        flash("No time traveling dishes please.", "bad_date")
        return redirect(f"/recipe/edit/{id}")
    Recipe.update(request.form)
    flash("Recipe updated!", "recipe_update")
    return redirect('/dashboard')

@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
    if not session:
        return redirect('/')
    # check to see if user = logged in and if logged in user = user that created recipe
    if session['user_id'] != Recipe.get_by_id({"id":id}).user_id:
        flash("Your not allowed in there. Please don't tamper with other peoples things.", "bad_edit")
        return redirect('/dashboard')
    Recipe.delete({"id": id})
    flash("Recipe deleted!", "recipe_delete")
    return redirect('/dashboard')

@app.route('/dashboard')
def recipe_dashboard():
    if not session:
        return redirect('/')
    return render_template("dashboard.html", active_user = User.get_by_id({"id":session['user_id']}), recipes = Recipe.get_all())