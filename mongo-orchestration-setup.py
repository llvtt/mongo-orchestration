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

#   echo curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"name\": \"mongod\", \"procParams\": {$TEST_PARAMS \"port\": 27017, \"dbpath\": \"$DATAPATH\", \"logpath\":\"$LOGPATH/mongo.log\", \"ipv6\":true, \"logappend\":true, \"journal\": true}}" http://localhost:8889/hosts
#   curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"name\": \"mongod\", \"procParams\": { $TEST_PARAMS \"port\": 27017, \"dbpath\": \"$DATAPATH\", \"logpath\":\"$LOGPATH/mongo.log\", \"ipv6\":true, \"logappend\":true, \"journal\": true}}" http://localhost:8889/hosts
#   echo curl -i -H "Accept: application/json" -X GET http://localhost:8889/hosts
#   curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/hosts




# echo "-------------------------------------------------------"
# echo "Server: $1"
# echo "Configuration: $2"
# echo "Authentication: $3"
# echo "SSL: $4"
# echo "-------------------------------------------------------"

# if [ "$1" == "22-release" -o "$1" == "20-release" ]; then
#   TEST_PARAMS='"vv" : true, '
# elif [ "$1" == "24-release" ]; then
#   TEST_PARAMS='"setParameter" : "textSearchEnabled=true", "vv" : true, '
# else
#   TEST_PARAMS='"setParameter":"enableTestCommands=1", "vv" : true, '
# fi

# if [ "$3" == "auth" ]; then

#   AUTH_PARAMS='"login":"bob", "password": "pwd123", "auth_key": "secret",'

# else

#   AUTH_PARAMS=""

# fi

# if [ "$4" == "ssl" ]; then
#   echo "Using SSL"
#   export SSL_PARAMS='"sslParams": {"sslMode": "requireSSL", "sslAllowInvalidCertificates" : true, "sslPEMKeyFile":"/mnt/jenkins/mongodb/ssl/ssl-files/server.pem", "sslCAFile": "/mnt/jenkins/mongodb/ssl/ssl-files/ca.pem", "sslWeakCertificateValidation" : true},'
# else
#   export SSL_PARAMS=""
# fi


# echo "TEST_PARAMS=$TEST_PARAMS"
# echo "AUTH_PARAMS=$AUTH_PARAMS"
# echo "SSL_PARAMS=$SSL_PARAMS"


# export DATAPATH="/mnt/jenkins/data"
# export LOGPATH="$WORKSPACE/log"
# echo "LOGPATH=$LOGPATH"
# mkdir -p "$LOGPATH"
# #echo "ls -ld LOGPATH"
# #ls -ld $LOGPATH

# echo "-------------------------------------------------------"
# echo "MongoDB Configuration: $2"
# echo "-------------------------------------------------------"

# date
# if [ "$2" == "single_server" ]; then
#   echo curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"name\": \"mongod\", \"procParams\": {$TEST_PARAMS \"port\": 27017, \"dbpath\": \"$DATAPATH\", \"logpath\":\"$LOGPATH/mongo.log\", \"ipv6\":true, \"logappend\":true, \"journal\": true}}" http://localhost:8889/hosts
#   curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"name\": \"mongod\", \"procParams\": { $TEST_PARAMS \"port\": 27017, \"dbpath\": \"$DATAPATH\", \"logpath\":\"$LOGPATH/mongo.log\", \"ipv6\":true, \"logappend\":true, \"journal\": true}}" http://localhost:8889/hosts
#   echo curl -i -H "Accept: application/json" -X GET http://localhost:8889/hosts
#   curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/hosts

# elif [ "$2" == "replica_set" ]; then
  
#   echo curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"id\": \"repl0\", \"members\":[{\"rsParams\":{\"priority\": 99}, \"procParams\": {$TEST_PARAMS \"dbpath\":\"$DATAPATH/db27017\", \"port\": 27017, \"logpath\":\"$LOGPATH/\
# db27017.log\", \"journal\": true, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, {\"rsParams\": {\"priority\": 1.1}, \"procParams\":{$TEST_PARAMS \"dbpath\":\
# \"$DATAPATH/db27018\", \"port\": 27018, \"logpath\":\"$LOGPATH/db27018.log\", \"journal\": true, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, \
# {\"procParams\":{$TEST_PARAMS \"dbpath\":\"$DATAPATH/db27019\", \"port\": 27019, \"logpath\":\"$LOGPATH/27019.log\", \"journal\": true, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}]}" http://localhost:8889/rs
#   curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"id\": \"repl0\", \"members\":[{\"rsParams\":{\"priority\": 99}, \"procParams\": {$TEST_PARAMS \"dbpath\":\"$DATAPATH/db27017\", \"port\": 27017, \"logpath\":\"$LOGPATH/db270\
# 17.log\", \"journal\": true, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, {\"rsParams\": {\"priority\": 1.1}, \"procParams\":{$TEST_PARAMS \"dbpath\":\"$DA\
# TAPATH/db27018\", \"port\": 27018, \"logpath\":\"$LOGPATH/db27018.log\", \"journal\": true, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, {\"pr\
# ocParams\":{\"dbpath\":\"$DATAPATH/db27019\", \"port\": 27019, \"logpath\":\"$LOGPATH/27019.log\", \"journal\": true, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}]}" http://localhost:8889/rs
#   echo curl -i -H "Accept: application/json" -X GET http://localhost:8889/rs/repl0/primary
#   curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/rs/repl0/primary

# elif [ "$2" == "sharded" ]; then
#   echo curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"routers\": [{$TEST_PARAMS \"port\": 27017, \"logpath\": \"$LOGPATH/router27017.log\"}], \"configsvrs\": [{\"port\": 27016, \"dbpath\": \"$DATAPATH/db27016\", \"logpath\": \"$LOGPATH/configsvr27016.log\"}], \"id\": \"shard_cluster_1\", \"members\": [{\"id\": \"sh01\", \"shardParams\": {\"procParams\": {$TEST_PARAMS \"port\": 27020, \"dbpath\": \"$DATAPATH/db27020\", \"logpath\":\"$LOGPATH/db27020.log\", \"ipv6\":true, \"logappend\":true, \"journal\": true}}}]}" http://127.0.0.1:8889/sh
#   curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"routers\": [{$TEST_PARAMS \"port\": 27017, \"logpath\": \"$LOGPATH/router27017.log\"}], \"configsvrs\": [{\"port\": 27016, \"dbpath\": \"$DATAPATH/db27016\", \"logpath\": \"$LOGPATH/configsvr27016.log\"}], \"id\": \"shard_cluster_1\", \"members\": [{\"id\": \"sh01\", \"shardParams\": {\"procParams\": {$TEST_PARAMS \"port\": 27020, \"dbpath\": \"$DATAPATH/db27020\", \"logpath\":\"$LOGPATH/db27020.log\", \"ipv6\":true, \"logappend\":true, \"journal\": true}}}]}" http://127.0.0.1:8889/sh
#   echo curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/sh/shard_cluster_1
#   curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/sh/shard_cluster_1

# fi
