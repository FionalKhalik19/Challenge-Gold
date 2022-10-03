import re
import sqlite3
import pandas as pd

from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'contoh API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'contoh Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

conn = sqlite3.connect('data/challenge_gold.db', check_same_thread=False)

conn.execute('''CREATE TABLE IF NOT EXISTS data (text varchar(100), text_clean varchar(100));''')

@swag_from("docs/contoh_text.yml", methods=['POST'])
@app.route('/contoh_text', methods=['POST'])
def text_processing():

    text = request.form.get('text')
    
    text_clean = re.sub(r'[^a-z]|#/S+|(\(.*\))|(\[.*\])|\n', ' ', text)

    conn.execute("INSERT INTO data (text, text_clean) VALUES ('" + text + "', '" + text_clean + "')")
    conn.commit()

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': text_clean,
    }
    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/contoh_file.yml", methods=['POST'])
@app.route("/contoh_file", methods=["POST"])
def file_processing():

    file = request.files.getlist('file')[0]
    data = pd.read_csv(file)
    variabel = data.text.to_list()
    nampung = []
    for variabel2 in variabel:
        text_clean = re.sub(r'[^a-z]', ' ', variabel2)
        conn.execute("INSERT INTO data (text, text_clean) VALUES ('" + variabel2 + "', '" + text_clean + "')")
        conn.commit()
        nampung.append(text_clean)

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': text_clean,
    }
    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()