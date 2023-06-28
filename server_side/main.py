from flask import Flask, render_template
import os
import dotenv
from src.modules import WorkerManager

### Load .env file
dotenv.load_dotenv(dotenv_path='../.env')
ADDRESS = os.getenv("ADDRESS")
PORT = os.getenv("PORT")
TEMPLATE_PATH = os.getenv("TEMPLATE_PATH")
STATIC_PATH = os.getenv("STATIC_PATH")
### End load .env file

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)


@app.after_request
def before_request(response):
    headers = {
        'Cache-Control': 'no-cache, no-store'
    }
    for header, value in headers.items():
        response.headers[header] = value

    return response


@app.route('/', methods=['GET'])
def process_root():
    return render_template('index.html')


@app.route('/api/test_api', methods=['GET'])
def process_test_api():
    return WorkerManager.handle_test_api()


if __name__ == '__main__':
    app.run(
        host=ADDRESS,
        port=PORT,
        debug=True
    )
