#
# elasticsearch-web-export
# Author: William Jimenez <wjimenez5271@gmail.com>
# License: GNU GPL 2.0
# Requires stash-query to do handle ElasticSearch interface: 
# https://github.com/robbydyer/stash-query
#

from flask import Flask, make_response, request, url_for
import subprocess
import os
import argparse

if not os.path.isfile('/usr/bin/stash-query'):
    raise Exception('Please ensure you have stash-query installed: https://github.com/robbydyer/stash-query')

app = Flask(__name__)


def do_query(start_time, end_time, query, es_host, output_file='/tmp/es-output.txt'):
    """
    Execute stash-query with parameters, and return results as string object
    :param start_time: Start time of query: e.g. 2015-03-20T10:36:47.621Z
    :param end_time: End time of query
    :param query: Query parameters, e.g. 'type:"saas_access"'
    :param output_file: tmp location for stash-query to write output to. We'll read the data from this location
    :return: str. results of query
    """
    cmd ="touch {0}".format(output_file)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    cmd = 'stash-query --connect_host {0} -s {1} -e {2} -q {3} -w {4}'.format(es_host, start_time,
                                                                              end_time, query, output_file)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    output, errors = p.communicate()
    if p.returncode or errors:
        # Print for debugging purposes to console
        print('Request Parameters: \n')
        print(start_time)
        print(end_time)
        print(query)
        print(errors)
        print(output)
    results = open(output_file, 'r')
    results_data = results.read()
    results.close()
    os.remove(output_file)
    return results_data


# Main interface to web service
@app.route('/')
def index():

    return '<b>ELK Data Export</b><p>' \
           'Hello. To construct a query, you\'ll need to create a URL like so: <p>' \
           '<pre>' \
           '[hostname:port]/query?start_time=2015-03-20T10:36:47.621Z&end_time=2015-03-20T10:40:47.621Z&query=type:"apache"' \
           '</pre>'

# Query interface
@app.route('/query')
def query():
    # Format response payload
    if len(request.args) == 0:
        return 'Error: Missing URL Parameters'
    response = make_response(do_query(request.args.get('start_time'),
                                      request.args.get('end_time'),
                                      request.args.get('query'),
                                      es_host))
    # Set headers
    response.headers["Content-Disposition"] = "attachment; filename=query_results.txt"
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export Elasticsearch data using an HTTP/web based interface')
    parser.add_argument("-h", "--es_host", help="elasticsearch host to query", required=False)
    args = parser.parse_args()
    global es_host
    es_host = args.es_host

    app.run(
        host="0.0.0.0",
        port=int("8085"),
        debug=True
    )
