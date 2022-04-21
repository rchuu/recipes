from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/add/recipe')
def add_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('add_recipe.html', user=User.get_from_id(data))


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/add/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "under_30": int(request.form["under_30"]),
        "date_made": request.form["date_made"],
        "user_id": session['user_id']
    }
    Recipe.save(data)
    return redirect('/success')


@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_recipe.html", edit=Recipe.get_one(data), user=User.get_from_id(user_data))


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/add/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "under_30": int(request.form["under_30"]),
        "date_made": request.form["date_made"],
        "id": request.form["id"]
    }
    Recipe.update(data)
    return redirect('/success')


@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("view_recipe.html", recipe=Recipe.get_one(data), user=User.get_from_id(user_data))


@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Recipe.destroy(data)
    return redirect('/success')
