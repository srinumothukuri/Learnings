import sys
import requests
import json
import random
from app import app
from flask import Flask, flash, request, jsonify
from topic import Topic
from monitor.networkutils import NetworkUtil
import pathlib
import time
# from cjsonencoder import CustomJSONEncoder


# app.json_encoder = CustomJSONEncoder

basedir = '/home/aryagami/new/billing_tools'
curdir = str(pathlib.Path(__file__).parent.absolute())


@app.route('/check_mml_connectivity', methods=['POST'])
def check_mml_connectivity():
    net_utils = NetworkUtil()
    content = net_utils.check_mml_login()
    content['status'] = 'success'
    return content


@app.route('/get_host_info', methods=['POST'])
def get_host_info():
    data = request.json
    if 'filePath' not in data.keys():
        return {"status": "file path is missing"}

    net_utils = NetworkUtil()
    content = net_utils.read_file_data(curdir + "/monitor/" + data['filePath'])
    content['status'] = 'success'
    return content


@app.route('/record_host_status', methods=['GET'])
def record_host_status():
    net_utils = NetworkUtil()
    content = net_utils.record_service_status(curdir + "/monitor/host_info")
    content['status'] = 'success'
    return content


@app.route('/get_topics', methods=['GET'])
def get_topics():
    rettopics = Topic.read_all_topics(basedir)
    if isinstance(rettopics, str):
        ret = {"status": rettopics}
    else:
        ret = {"status": "success", "result": rettopics}

    return ret


@app.route('/get_log_topics', methods=['GET'])
def get_log_topics():
    rettopics = Topic.read_all_log_topics(basedir)
    if isinstance(rettopics, str):
        ret = {"status": rettopics}
    else:
        ret = {"status": "success", "result": rettopics}

    return ret


@app.route('/run_query', methods=['POST'])
def run_query():
    data = request.json

    topic = Topic(data, basedir)
    results = topic.run_query()
    if isinstance(results, str):
        ret = {"status": results}
    else:
        ret = {"status": "success", "result": results}
    print("print query results %s" % (results))
    return ret


@app.route('/check_logs', methods=['POST'])
def check_logs():
    data = request.json
    topic = Topic(data, basedir)
    results = topic.run_logs_query()
    if isinstance(results, str):
        ret = {"status": results}
    else:
        ret = {"status": "success", "result": results}
    #print("print results %s" % (results))
    return str(ret)

@app.route('/check_debug_logs', methods=['POST'])
def check_debug_logs():
    data = request.json
    topic = Topic(data, basedir)
    results =topic.debug_query(data)
    if isinstance(results, str):
        ret ={"status": results}
        print('ret', ret)
    else:
        ret = {"status": "success", "result":results}
    return ret 

@app.route('/verify_nira_info', methods=['POST'])
def verify_nira_info():
    data = request.json
    topic = Topic(data, basedir)
    results = topic.run_billing_query()
    if isinstance(results, str):
        ret = {"status": results}
    else:
        ret = {"status": "success", "result": results}
    #print("print results %s" % (results))
    return str(ret)


@app.route('/check_ussd_codes', methods=['POST'])
def check_ussd_codes():
    data = request.json
    topic = Topic(data, basedir)
    dialogId = str(random.random()).split(".")[1]
    results = topic.run_ussd_query(dialogId)
    results = results.replace('<LF>', ' ').replace('&', '')
    if isinstance(results, str):
        ret = {"status": "success", "result": results}
    else:
        ret = {"status": "success", "result": results}
    #print("print results %s" % (results))
    return json.dumps(ret)

@app.route('/run_cmd_cmds', methods=['POST'])
def run_telnet_cmds():
    data = request.json
    topic = Topic(data,basedir)
    if data['query'] == "prepaid_to_postpaid" or data['query'] == "postpaid_to_prepaid":
       topic.deactivate_activate_sub("deactivate")
       print("Deactivated...")
       time.sleep(10)
       results = topic.run_telnet_cmds()
       time.sleep(5)
       topic.deactivate_activate_sub("status_activate")
       print("Activated successfully")
    else:
       results = topic.run_telnet_cmds()
    return  json.dumps(results)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        basedir = sys.argv[1]

    app.run(host="0.0.0.0", port=9001, threaded=True, debug=True)
