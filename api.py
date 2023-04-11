from flask import Flask, jsonify
from find_list import find_list
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abobus'
app.config['JSON_AS_ASCII'] = False


headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }

class IDError(Exception):
    pass


@app.route('/find_list')
def find_listt():
    return jsonify(find_list(headers=headers))
    

if __name__ == '__main__':
    app.run(port=8000, host="127.0.0.1", debug=True)
    