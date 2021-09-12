from flask_app.controllers import routes_users, routes_recipes
from flask_app import app

if __name__=="__main__":
    app.run(debug=True)