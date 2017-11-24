# External deps
import argparse
import logging
from flask import Flask, request
import lifxlan

# Internal deps
import pifx.flask_utils as flask_utils
from pifx.group import Group

##########################################################################
# MAIN
##########################################################################

app = Flask("pifx-api")

def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Hostname")
    parser.add_argument("port", type=int, help="Port")
    return parser.parse_args()

LAN = None
def main():
    global LAN

    args = options()
    LAN = lifxlan.LifxLAN()
    logging.basicConfig(level=logging.INFO)
    app.run(debug=False, host=args.host, port=args.port, processes=50)

@app.route('/', methods=["GET"])
def hello():
    def action():
        return "Hey! Listen"
    return flask_utils.wrapper(action)

##########################################################################
# DEVICES ROUTES
##########################################################################

@app.route('/devices/list', methods=["GET"])
def devices_list():
    def action():
        devices = [d.get_label() for d in LAN.get_devices()]
        return {"devices": devices}
    return flask_utils.wrapper(action)

##########################################################################
# GROUP ROUTES
##########################################################################

@app.route('/groups/list', methods=["GET"])
def groups_list():
    def action():
        return {"groups": Group.list_group(LAN)}
    return flask_utils.wrapper(action)

@app.route('/groups/stats', methods=["GET"])
def groups_stats():
    def action():
        return {"groups": Group.stats_group(LAN)}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/devices', methods=["GET"])
def group_get_devices(group_name):
    def action():
        group = Group(LAN, group_name)
        return {"devices": group.get_devices_label()}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/power', methods=["GET"])
def group_get_power(group_name):
    def action():
        group = Group(LAN, group_name)
        return {"power": group.get_power()}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/power/<value>', methods=["POST"])
def group_set_power(group_name, value):
    def action():
        group = Group(LAN, group_name)
        data = flask_utils.get_data(request.data)
        group.set_power(float(value), duration=data["duration"], wait=data["wait"])
        return {"success": True}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/color/<value>', methods=["POST"])
def group_set_color(group_name, value):
    def action():
        group = Group(LAN, group_name)
        data = flask_utils.get_data(request.data)
        group.set_color(float(value), duration=data["duration"], wait=data["wait"])
        return {"success": True}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/hue/<value>', methods=["POST"])
def group_set_hue(group_name, value):
    def action():
        group = Group(LAN, group_name)
        data = flask_utils.get_data(request.data)
        group.set_hue(float(value), duration=data["duration"], wait=data["wait"])
        return {"success": True}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/brightness/<value>', methods=["POST"])
def group_set_brightness(group_name, value):
    def action():
        group = Group(LAN, group_name)
        data = flask_utils.get_data(request.data)
        group.set_brightness(float(value), duration=data["duration"], wait=data["wait"])
        return {"success": True}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/saturation/<value>', methods=["POST"])
def group_set_saturation(group_name, value):
    def action():
        group = Group(LAN, group_name)
        data = flask_utils.get_data(request.data)
        group.set_saturation(float(value), duration=data["duration"], wait=data["wait"])
        return {"success": True}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/colortemp/<value>', methods=["POST"])
def group_set_colortemp(group_name, value):
    def action():
        group = Group(LAN, group_name)
        data = flask_utils.get_data(request.data)
        group.set_colortemp(float(value), duration=data["duration"], wait=data["wait"])
        return {"success": True}
    return flask_utils.wrapper(action)

@app.route('/group/<group_name>/infrared/<value>', methods=["POST"])
def group_set_infrared(group_name, value):
    def action():
        group = Group(LAN, group_name)
        data = flask_utils.get_data(request.data)
        group.set_infrared(float(value), duration=data["duration"], wait=data["wait"])
        return {"success": True}
    return flask_utils.wrapper(action)

##########################################################################
# MAIN BINDING
##########################################################################

if __name__ == "__main__":
    main()
