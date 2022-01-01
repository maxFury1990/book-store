from books_app.rest_api.flask_api import create_flask_app


def run_flask():
    app = create_flask_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run_flask()
