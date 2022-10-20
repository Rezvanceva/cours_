from main import app, create_and_config_app

app = create_and_config_app("config.py")


if __name__ == '__main__':
    app.run(port=80)