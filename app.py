import json

import requests
from flask import Flask, request, render_template, jsonify, send_from_directory

app = Flask(__name__, template_folder="templates", static_folder="static")


def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/receive-visitor-info', methods=['POST'])
def receive_visitor_info():
    data = request.json

    user_ip = request.remote_addr
    user_agent = request.user_agent.string

    ip_info = get_location(user_ip)
    print(ip_info)

    user_dict = {
        "IP": user_ip,
        "User Agent": user_agent,
        "Language": data["language"],
        "ScreenResolution": data["screenResolution"],
        "Browser": data["browser"],
        "City": ip_info["city"],
        "Region": ip_info["region"],
        "Country": ip_info["country"]
    }
    print(json.dumps(user_dict, indent=4))

    return jsonify({'message': 'Data received successfully'})


if __name__ == '__main__':
    app.run(debug=True)
