import json
import os
import shutil
import sys
import urllib
import urllib2


BASE_DIR="C:\\mongo"

def dbpath_for_port(port):
    return os.path.join(BASE_DIR, 'data', 'db%d' % port)

def logpath_for_port(port):
    return os.path.join(BASE_DIR, 'logs', 'mongodb-%d.log' % port)

def params_for_port(port):
    return {
        'port': port,
        'dbpath': dbpath_for_port(port),
        'logpath': logpath_for_port(port)
    }

def main():
    # These arguments and their defaults match the interface of the Bourne shell
    # script that performs the same action on *nix machines.
    if len(sys.argv) < 3:
        print("USAGE: mongo-orchestration-setup.py <server_version> "
              "<configuration> [enable_auth] [enable_ssl]")
        sys.exit(2)

    server_version = sys.argv[1]
    configuration = sys.argv[2]
    if len(sys.argv) >= 4:
        enable_auth = (sys.argv[3] == 'auth')
    else:
        enable_auth = False
    if len(sys.argv) >= 5:
        enable_ssl = (sys.argv[4] == 'ssl')
    else:
        enable_ssl = False

    # Set test commands and verbose logging
    test_params = {'vv': True}
    if server_version == '24-release':
        test_params['setParameter'] = 'textSearchEnabled=true'
    elif server_version not in ('20-release', '22-release'):
        test_params['setParameter'] = 'enableTestCommands=1'

    # Set auth
    auth_params = {}
    if enable_auth:
        auth_params = {'login': 'bob',
                       'password': 'pwd123',
                       'auth_key': 'secret'}

    # Set SSL
    ssl_params = {}
    if enable_ssl:
        key_file = os.path.join(
            BASE_DIR, "mongodb", "ssl", "ssl-files", "server.pem")
        ca_file = os.path.join(
            BASE_DIR, "mongodb", "ssl", "ssl-files", "ca.pem")
        ssl_params = {
            'sslParams': {
                'sslMode': 'requireSSL',
                'sslAllowInvalidCertificates': True,
                'sslPEMKeyFile': key_file,
                'sslCAFile': ca_file,
                'sslWeakCertificateValidation': True}}

    print("TEST PARAMS: %r" % test_params)
    print("AUTH PARAMS: %r" % auth_params)
    print("SSL PARAMS : %r" % ssl_params)

    def insert_test_auth_ssl(params):
        for pset in (test_params, auth_params, ssl_params):
            params.update(pset)

    shutil.rmtree(BASE_DIR, ignore_errors=True)

    request_url = "http://localhost:8889"
    base_params = {'ipv6': True, 'nojournal': True, 'logappend': True,
                   'noprealloc': True, 'smallfiles': True}
    entity_id = ""
    if configuration == 'single_server':
        proc_params = base_params.copy()
        proc_params.update(params_for_port(27017))
        proc_params.update(test_params)
        configuration = {
            'name': 'mongod',
            'procParams': proc_params}
        request_url += '/hosts'
    elif configuration == 'replica_set':
        entity_id = "repl0"
        configuration = {'id': entity_id}

        rs_params1 = {'rsParams': {'priority': 99}}
        rs_params2 = {'rsParams': {'priority': 1.1}}

        proc_params1 = base_params.copy()
        proc_params1.update(params_for_port(27017))
        proc_params1.update(test_params)
        rs_params1['procParams'] = proc_params1

        proc_params2 = base_params.copy()
        proc_params2.update(params_for_port(27018))
        proc_params2.update(test_params)
        rs_params2['procParams'] = proc_params1

        proc_params3 = base_params.copy()
        proc_params3.update(params_for_port(27019))
        proc_params3.update(test_params)

        configuration['members'] = [rs_params1, rs_params2, proc_params3]

        request_url += '/rs'
    elif configuration == 'sharded':
        entity_id = "shard_cluster_1"
        configuration = {'id': entity_id}

        config_params = base_params.copy()
        config_params.update(params_for_port(27016))

        proc_params = base_params.copy()
        proc_params.update(params_for_port(27020))

        configuration['members'] = [
            {'id': 'sh01',
             'shardParams': {
                 'procParams': proc_params}}]

        request_url += '/sh'
    else:
        print("Unrecognized configuration: %s" % configuration)
        sys.exit(1)

    configuration.update(auth_params)
    configuration.update(ssl_params)


    request_body = json.dumps(configuration)
    request = urllib2.Request(request_url,
                              data=request_body,
                              headers={'Accept': 'application/json'})
    print("Sending %s to %s..." % (request_body, request_url))
    response = urllib2.urlopen(request)
    print(response.read())
    get_url = "%s/%s" % (request_url, entity_id) if entity_id else request_url
    response = urllib2.urlopen(get_url)
    print(response.read())

if __name__ == '__main__':
    main()
