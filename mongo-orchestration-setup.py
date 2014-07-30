import json
import os
import shutil
import urllib
import urllib2


BASE_DIR="C:\mongo"

def dbpath_for_port(port):
    return os.path.join(BASE_DIR, 'data', 'db%d' % port)

def logpath_for_port(port):
    return os.path.join(BASE_DIR, 'logs', 'mongodb-%d.log' % port)

def main():
    shutil.rmtree(BASE_DIR, ignore_errors=True)

    for port in range(27017, 27020):
        os.makedirs(dbpath_for_port(port))

    # Assume single-server setup for now
    http_data = {"name": "mongod",
                 "procParams": {"port": 27017,
                                "dbpath": dbpath_for_port(27017),
                                "logpath": logpath_for_port(27017),
                                "ipv6": True,
                                "logappend": True,
                                "nojournal": True}}
    request_body = json.dumps(http_data)
    request_url = 'http://localhost:8889/hosts'
    request = urllib2.Request(request_url,
                              data=request_body,
                              headers={'Accept': 'application/json'})
    print("Sending %s to %s..." % (request_body, request_url))
    response = urllib2.urlopen(request)
    print(response.read())
    response = urllib2.urlopen(request_url)
    print(response.read())

if __name__ == '__main__':
    main()
