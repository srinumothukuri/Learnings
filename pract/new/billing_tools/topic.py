import json
import os
import requests
from database import Database
from string import Template
import traceback
from flask import jsonify, make_response
import subprocess
#import paramiko
import telnetlib
from io import StringIO
import time

class Topic:
    def __init__(self, data, basedir):
        self.data = data
        self.topic_name = None
        self.query_name = None
        self.topic_data = None
        self.query_data = None
        self.basedir = basedir

    @staticmethod
    def read_all_topics(basedir):
        topics = {}
        for root, dirs, files in os.walk("/home/ubuntu/new/billing_tools" + "/topics"):
            for filename in files:
                queries = []
                if filename != 'log_check':
                    with open('/home/ubuntu/new/billing_tools' + '/topics/' + filename) as f:
                        # print(f)
                        try:
                            topic_data = json.load(f)
                        except:
                            traceback.print_exc()
                            return "Topic definition error: " + filename

                        for query, value in topic_data.items():
                            if value :
                                queryv = {"query": query,
                                        "params": value['input_params'],
                                        "server_name": value
                                        }
                                queries.append(queryv)
                            else :
                                aqueryv = {"query": query,
                                            "params": value['input_params']
                                        }
                                queries.append(queryv)
                        topics[filename] = {'queries': queries}
        return topics

    def read_all_log_topics(basedir):
        topics = {}
        for root, dirs, files in os.walk("/home/ubuntu/new/billing_tools" + "/topics"):
            for filename in files:
                queries = []
                if filename == 'log_check':
                    with open('/home/ubuntu/new/billing_tools' + '/topics/' + filename) as f:
                        # print(f)
                        try:
                            topic_data = json.load(f)
                        except:
                            traceback.print_exc()
                            return "Topic definition error: " + filename

                        for query, value in topic_data.items():
                            # print("value", value)
                            queryv = {"query": query,
                                      "params": value['issue_types']}
                            queries.append(queryv)
                        topics[filename] = {'queries': queries}
        return topics
    def read_billing_topics(basedir):
        topics = {}
        for root, dirs, files in os.walk(basedir + "/topics"):
            for filename in files:
                queries = []
                if filename == 'registration':
                    with open(basedir + '/topics/' + filename) as f:
                        # print(f)
                        try:
                            topic_data = json.load(f)
                        except:
                            traceback.print_exc()
                            return "Topic definition error: " + filename

                        for query, value in topic_data.items():
                            # print("value", value)
                            queryv = {"query": query,
                                      "params": value}
                            queries.append(queryv)
                        topics[filename] = {'queries': queries}
        return topics

    def _validate_data(self):
        if 'topic' in self.data:
            self.topic_name = self.data['topic']
        else:
            return 'Topic not specified'

        if 'query' in self.data:
            self.query_name = self.data['query']
        else:
            return 'Query not specified'

        with open(self.basedir + '/topics/' + self.topic_name) as f:
            self.topic_data = json.load(f)

        if self.query_name not in self.topic_data:
            return "Query not defined in topic: " + self.query_name
        self.query_data = self.topic_data[self.query_name]

        for iparam in self.query_data['input_params']:
            if iparam not in self.data:
                return "Input param " + iparam + " missing"

        return "Pass"

    def run_query(self):
        ret = self._validate_data()
        if ret != 'Pass':
            return ret

        db_conns = {}
        results = []
        for query in self.query_data['state_queries']:
            state = query['state_name']
            db_name = query['db_name']
            if db_name not in db_conns:
                db_conn = Database(query['repo_name'],
                                   'billing', 'access', db_name)
                ret = db_conn.connect()
                if ret != "Success":
                    return "Connection to " + query['repo_name'] + " failed"
                db_conns[db_name] = db_conn
            else:
                db_conn = db_conns[db_name]
            try:
                qresult = db_conn.run_query(query['query'], self.data)
            except:
                results.append(
                    {'state_name': state, 'status': "Could not run query"})
                traceback.print_exc()
                return results

            qresult['status'] = 'success'
            results.append(
                {'state_name': state, 'status': 'success', 'result': qresult})
            if 'out_params' in query and len(query['out_params']) != 0:
                if len(qresult['entries']) == 0:
                    return "Could not extract out params from query: " + state
                for out_param in query['out_params']:
                    opindex = qresult['fields'].index(out_param)
                    self.data[out_param] = qresult['entries'][0][opindex]

        for db_name, db_conn in db_conns.items():
            db_conn.close()

        return results


    def deactivate_activate_sub(self,state):

        isdn = self.data['ISDN']

        SERVER_URL='http://10.20.15.12/billing'

        SESSIONID_command = "mysql -h billingrepo -u billing -paccess billing -s --execute \"select session_key from session where user_role = 'admin' order by date desc limit 1;\""

        process = subprocess.Popen(SESSIONID_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error = process.communicate()

        SESSIONID = output.decode('utf-8').strip()

        SUB_ID_command = f"mysql -h billingrepo -u billing -paccess billing -s --execute \"set session transaction isolation level read uncommitted; select subscription_id from subscription where served_MSISDN='{isdn}' order by created_date desc limit 1;\""

        # Execute the command using subprocess
        process = subprocess.Popen(SUB_ID_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        output, error = process.communicate()
        SUB_ID=output.decode('utf-8').strip()

        if process.returncode != 0:
           print(f"Error: {error.decode('utf-8')}")
           exit()

        command = f"curl -X POST -H 'Content-Type: application/json' -H 'SESSIONID:{SESSIONID}' -i '{SERVER_URL}/{state}/' --data '{{\"entityName\":\"subscription\",\"activationId\":\"{SUB_ID}\",\"reason\":\"subscription conversion\"}}'"
        print(command)
        #Execute the command using subprocess
        try:
           result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
           output = result.stdout.decode('utf-8') if result.stdout else None
           print("Command output:", output)

        except subprocess.CalledProcessError as e:
           print("Command execution failed:", e)
           exit()

    def run_telnet_cmds(self):
        ret = self._validate_data()
        if ret != 'Pass':
            return ret
        print("Trying to connect...")
        HOST = "10.20.30.139"
        PORT = "7776" 
        try :
            tn = telnetlib.Telnet(HOST,PORT,timeout=10)
            print("connected")
        except Exception as e:
            print(f"Telnet connection failed: {e}")
            exit()
        try:
            login_command = b'LGI:HLRSN=1,OPNAME="jeelani",PWD="js@yed@2016";\n'
            print(login_command)
            tn.write(login_command)
        except Exception as e:
            print(f"Login failed: {e}")
            exit()        
        out=''    
        while True:
            try:
                response = tn.read_until(b'\n')
                out += (response.decode('utf-8'))
                if b'---    END' in  response:
                    out += "\n"
                    break
            except EOFError:
                break

        time.sleep(3)
        qresult=[]
        for query in self.query_data['state_queries']:
            command = query['command']
            isdn = self.data['ISDN']
            if 'ADD' in command:
                db_conn = Database('billingrepo', 'billing', 'access', 'billing')
                ret = db_conn.connect()
                if ret != "Success":
                    return "Connection to billingrepo failed"
                try:
                     tplid,imsi = db_conn.run_telnet_sql(query['query1'],query['query2'],self.data)
                except Exception as e:
                    print(f"mysql connection failed: {e}")
                    exit()
                cmd = command.format(tplid=tplid,isdn=isdn,imsi=imsi)
                print(cmd)
                up_cmd = cmd.encode('utf-8')
            else:
                cmd = command.format(isdn=isdn)
                print(cmd)
                up_cmd = cmd.encode('utf-8')
            try:
                tn.write(up_cmd)
            except Exception as e:
                print(f"Query execution failed: {e}")
                exit()

            output=''
            while True:
                try:
                    response = tn.read_until(b'\n')
                    output += (response.decode('utf-8'))
                    if b'---    END' in  response:
                        output += "\n"
                        break
                except EOFError:
                    break
            qresult.append(output)

            time.sleep(3)
    
        tn.close()
        return qresult

    def debug_query(self,data):
        ret = self._validate_data()
        if ret != 'Pass':
            return ret

        results = []
        f = open('/home/ubuntu/keypair','r')
        s = f.read()
        keyfile = StringIO(s)
        mykey = paramiko.RSAKey.from_private_key(keyfile)
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(self.query_data)
        for query in self.query_data['state_queries']:
            input_params = data['filter']
            user_name = query['userName']
            server_name = query['server_name']
            command = query['command']
            if query['input_params'] == 'Yes':
                qu_cmd = command + input_params
            else:
                qu_cmd = command    
            ssh.connect(server_name, username=user_name, pkey=mykey)
            stdin, stdout, stderr = ssh.exec_command(qu_cmd)
            outlines=stdout.readlines()
            resp=''.join(outlines)
            print(resp)
            results.append(resp)
        return (json.dumps(results))

    def _validate_log_query(self):
        if 'topic' in self.data:
            self.topic_name = self.data['topic']
        else:
            return 'Topic not specified'

        if 'query' in self.data:
            self.query_name = self.data['query']
        else:
            return 'Query not specified'

        with open(self.basedir + '/topics/' + self.topic_name) as f:
            self.topic_data = json.load(f)

        if self.query_name not in self.topic_data:
            return "Query not defined in topic: " + self.query_name
        self.query_data = self.topic_data[self.query_name]

        return "Pass"
    def _validate_billing_query(self):
        if 'topic' in self.data:
            self.topic_name = self.data['topic']
        else:
            return 'Topic not specified'

        if 'query' in self.data:
            self.query_name = self.data['query']
        else:
            return 'Query not specified'

        with open(self.basedir + '/topics/' + self.topic_name) as f:
            self.topic_data = json.load(f)

        if self.query_name not in self.topic_data:
            return "Query not defined in topic: " + self.query_name
        self.query_data = self.topic_data[self.query_name]

        return "Pass"

    def prepare_login_with_grep_command(self, instances, log_file_name, key_name, lines_before, lines_after, sub_filters):
        commands = []
        for instance in instances:
            command = "ssh -i ~/keypair ubuntu@{} sudo cat {} | grep -B {} -A {} --binary-files=text '{}'".format(
                instance, log_file_name, lines_before, lines_after, key_name)
            if sub_filters:
                for sub_filter in sub_filters:
                    further_filter_command = (
                        command + "| grep --binary-files {}".format(sub_filter))
                    commands.append(further_filter_command)
            else:
                commands.append(command)
        return commands

    def run_logs_query(self):
        ret = self._validate_log_query()
        if ret != 'Pass':
            return ret

        results = []
        match_param = []
        for query in self.data['pattern']['log_searches']:
            input_params = self.data['input_params']
            moducle = query['module']
            server_names = query['server_name']
            file_path = query['file_path']
            matchParam = query['filter_strigs']
            sub_topic_issue = query['sub_topic_issue']
            sub_filters = query["sub_filters"]
            if sub_topic_issue and sub_topic_issue == 'NIRA not working':
                # need to add caching in dict date wise
                commands = self.prepare_login_with_grep_command(
                    frozenset(server_names.split(",")), file_path, matchParam, input_params[1], input_params[2])
                for command in commands:
                    results.append(
                        subprocess.check_output(command, shell=True))
            else:
                for connection in server_names:
                    url = "http://" + \
                        connection.strip('"') + ":6090/check_logs"
                    print("URL", url)
                    try:
                        ret = requests.post(url, json={
                                            'pattern': input_params, 'file_path': file_path, 'matchParam': matchParam, 'sub_topic_issue': sub_topic})
                        response = ret.json()
                        results.append(
                            {'module': module, 'status': 'success', 'result': response["result"]})
                    except requests.exceptions.ConnectionError:
                        results.append(
                            {'module': module, 'status': 'Connection refused'})
            return results

    def run_billing_query(self):
        ret = self._validate_billing_query()
        if ret != 'Pass':
            return ret
        results = []
        match_param = []
        server_names = self.data['queries']['server_name']
        for connection in server_names:
                    url = "http://" + \
                        connection.strip('"') + ":8080/billing/verify_nira_info/"
                    print("URL", url)
                    try:
                        ret = requests.post(url, json={
                                            'pattern': self.data['inputParam']})
                        response = ret.json()
                        results.append(
                            {'status': 'success', 'result': response["result"]})
                    except requests.exceptions.ConnectionError:
                        results.append(
                            {'status': 'Connection refused'})
        return results
    

    def run_ussd_query(self, dialogid):
        ret = self._validate_billing_query()
        if ret != 'Pass':
            return ret
        match_param = []
        ussd_code = self.data['inputParam']["ussd_code"]
        msisdn = self.data['inputParam']["servedMSISDN"]
        server_names = ["ussd"]
        for connection in server_names:
                    url = "http://{}:8007/service3?dialogid={}&ussdstring={}&msisdn={}".format(connection.strip('"'),dialogid,ussd_code,msisdn)
                    print("URL", url)
                    try:
                        ret = requests.get(url)
                        print("status code>>>>" + str(ret.status_code))
                        response = ret.text
                        print(response)
                        return response
                    except requests.exceptions.ConnectionError:
                        response = "Connection refused"
        return response
