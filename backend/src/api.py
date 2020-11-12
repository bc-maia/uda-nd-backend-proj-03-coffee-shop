from typing import Text
from flask import Flask, request, jsonify, abort
from flask import json
from flask.wrappers import Response
from sqlalchemy import exc
from flask_cors import CORS
from models import Drink
from database import db_drop_and_create_all, setup_db
from auth import AuthError, requires_auth


def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    TODO-DONE: uncomment the following line to initialize the database
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    """
    # db_drop_and_create_all()

    """
    ROUTES
    """

    """
    TODO-DONE: implement endpoint
        GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks or appropriate status code
        indicating reason for failure
    """

    @app.route("/drinks")
    def drinks():
        if drinks := Drink.all():
            return jsonify({"success": True, "drinks": drinks})
        else:
            abort(404)

    """
    TODO-DONE: implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks or appropriate status code
        indicating reason for failure
    """

    @app.route("/drinks-detail")
    def drinks_detail():
        if drinks := Drink.all(True):
            return jsonify({"success": True, "drinks": drinks})
        else:
            abort(404)

    """
    TODO-DONE: implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink or
        appropriate status code indicating reason for failure
    """

    @app.route("/drinks", methods=["POST"])
    def add_drink():
        payload = request.get_json()
        title = payload["title"]
        if drink := Drink.find_by(title):
            abort(
                Response(
                    response=f"Drink '{title}' already exists!",
                    status=405,
                )
            )
        else:
            recipe = json.dumps(payload["recipe"])
            drink = Drink(title=title, recipe=recipe)
            drink.insert()
            return jsonify({"success": True, "drinks": drink.long()})

    """
    TODO-DONE: implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink or appropriate
        status code indicating reason for failure
    """

    @app.route("/drinks/<id>", methods=["PATCH"])
    def update_drink(id):
        payload = request.get_json()
        if drink := Drink.find(id):
            if title := payload["title"]:
                drink.title = title
            if recipe := payload["recipe"]:
                drink.recipe = json.dumps(recipe)
            drink.update()
            return jsonify({"success": True, "drinks": drink.long()})
        else:
            abort(404)

    """
    TODO-DONE: implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record or appropriate status code
        indicating reason for failure
    """

    @app.route("/drinks/<id>", methods=["DELETE"])
    def remove_drink(id):
        if drink := Drink.find(id):
            drink.delete()
            return jsonify({"success": True, "delete": id})
        else:
            abort(404)

    """
    Error Handling
    """

    def format_handler(message: str, status: int) -> any:
        return (
            jsonify(
                {
                    "success": False,
                    "message": message,
                    "error": status,
                }
            ),
            status,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return format_handler("bad request", 400)

    """
    TODO-DONE: implement error handler for 404
        error handler should conform to general task above
    """

    @app.errorhandler(404)
    def not_found(error):
        return format_handler(message="resource not found", status=404)

    @app.errorhandler(405)
    def not_allowed(error):
        return format_handler("method not allowed", 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return format_handler("unprocessable", 422)

    """
    TODO: implement error handler for AuthError
        error handler should conform to general task above
    """

    @app.errorhandler(401)
    def unauthorized(error):
        return format_handler("unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(error):
        return format_handler("forbidden", 403)

    return app
