from flask import Flask
from flask import jsonify

app = Flask(__name__)
URL_ROOT = '/api/v1'

employee_list = [
    {
        "name": "John",
        "age": 39,
    },
    {
        "name": "Joe",
        "age": 27,
    },
    {
        "name": "Lily",
        "age": 29
    }
]


@app.route(URL_ROOT + "/employees", methods=['GET'])
def get_all_employees():
    return jsonify(employee_list), 200


@app.route(URL_ROOT + "/employee/<name>", methods=['GET'])
def get_employee_by_name(name=None):
    if name is None:
        return {}, 404
    else:
        res = list(filter(lambda x: (str(x['name']).upper() == name.upper()), employee_list))
        if res:
            return res[0], 200
        else:
            return {}, 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True, port=80)
