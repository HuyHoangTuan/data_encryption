from flask import Flask, render_template, request, make_response, abort
import os
import dotenv
from flask_cors import CORS
from src.modules import WorkerManager

### Load .env file
dotenv.load_dotenv(dotenv_path='../.env')
ADDRESS = os.getenv("ADDRESS")
PORT = os.getenv("PORT")
TEMPLATE_PATH = os.getenv("TEMPLATE_PATH")
STATIC_PATH = os.getenv("STATIC_PATH")
### End load .env file

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)
CORS(app, origins='*')

@app.after_request
def after_request(response):
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

@app.route('/api/compress_audio', methods=['POST'])
def process_compress_audio():
    file = None
    subbands = request.form.get('subbands')
    samples = request.form.get('samples')
    
    for index, fileName in enumerate(request.files):
        file = request.files[fileName]
        if index == 0:
            break
            
    if file != None:
        if subbands is None: subbands = 32
        if samples is None: samples = 36
        data = WorkerManager.handle_compress_audio(file=file, subbands= subbands, samples= samples)
        # print(data)
        response = make_response(data)
        response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Disposition'] = 'inline; filename=result.png'
        return response
    else:
        return abort(415, 'Unsupported Media Type')

if __name__ == '__main__':
    app.run(
        host=ADDRESS,
        port=PORT,
        debug=True
    )
