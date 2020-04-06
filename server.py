from flask import Flask, request, jsonify
import psycopg2
from string import capwords

from config import db_postgre_config

TOKEN = '37219db3-d3d5-436b-9ae9-3ea6978b2ca0'
KEYWORD = 'keyword'
AUTH_TOKEN = 'auth_token'
app = Flask(__name__)


@app.route('/')
def hello_world():
    return ''


@app.route('/search', methods=['POST'])
def search_road():
    conn = None
    data = request.form.to_dict()
    if AUTH_TOKEN not in data or data[AUTH_TOKEN] != TOKEN:
        return jsonify(error=True, message='Not authenticated', result=[])
    if KEYWORD not in data or data[KEYWORD] == '':
        return jsonify(error=True, message='Please input a keyword', result=[])
    search_string = data[KEYWORD]
    data_to_return = []
    try:
        params = db_postgre_config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        cur.execute(f"SELECT * FROM road WHERE name LIKE '%{search_string.lower()}%' LIMIT 5")
        results = cur.fetchall()

        for result in results:
            data_to_return.append({'name': capwords(result[1]), 'description': result[2].capitalize()})
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return jsonify(error=True, message='Something went wrong', result=error)
    finally:
        if conn is not None:
            conn.close()
            return jsonify(error=False, message='', result=data_to_return)
        else:
            return jsonify(error=True, message='Something went wrong', result=[])
