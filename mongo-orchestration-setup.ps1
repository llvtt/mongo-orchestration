param([string]$server, [string]$configuration, [string]$authentication="noauth", [string]$ssl="nossl")

echo "-------------------------------------------------------"
echo "Server: $server"
echo "Configuration: $configuration"
echo "Authentication: $authentication"
echo "SSL: $ssl"
echo "-------------------------------------------------------"

# Note: backslashes must be escaped in the following string:
$DATAPATH="C:\\mongo\\data"
# Note: backslashes must be escaped in the following string:
$SSL_FILES_ROOT="C:\\Users\\Luke\\code\\mongo-orchestration\\ssl-files"
# TODO: this variable will be injected
$WORKSPACE="C:\\mongo"
# Note: backslashes must be escaped in the following string:
$LOGPATH="$WORKSPACE\\log"

md "$DATAPATH\db27016"
md "$DATAPATH\db27017"
md "$DATAPATH\db27018"
md "$DATAPATH\db27019"
md "$WORKSPACE\logs"

if (($server -eq "22-release") -Or ($server -eq "20-release")) {
    $TEST_PARAMS='"vv" : true, '
} elseif ($server -eq "24-release") {
    $TEST_PARAMS='"setParameter" : "textSearchEnabled=true", "vv" : true, '
} else {
    $TEST_PARAMS='"setParameter":"enableTestCommands=1", "vv" : true, '
}

if ($authentication -eq "auth") {
    $AUTH_PARAMS='"login":"bob", "password": "pwd123", "auth_key": "secret",'
}

if ($ssl -eq "ssl") {
   echo "Using SSL"
   $SSL_PARAMS='"sslParams": {"sslMode": "requireSSL", "sslAllowInvalidCertificates" : true, "sslPEMKeyFile":"$SSL_FILES_ROOT\\server.pem", "sslCAFile": "$SSL_FILES_ROOT\\ca.pem", "sslWeakCertificateValidation" : true},'
}

echo "TEST_PARAMS=$TEST_PARAMS"
echo "AUTH_PARAMS=$AUTH_PARAMS"
echo "SSL_PARAMS=$SSL_PARAMS"

echo "-------------------------------------------------------"
echo "MongoDB Configuration: $configuration"
echo "-------------------------------------------------------"

$http_request = New-Object -ComObject Msxml2.XMLHTTP
if ($configuration -eq "single_server") {
    $url = "http://localhost:8889/hosts"
    $request_body="{$AUTH_PARAMS $SSL_PARAMS `"name`": `"mongod`", `"procParams`": {$TEST_PARAMS `"port`": 27017, `"dbpath`": `"$DATAPATH`", `"logpath`":`"$($LOGPATH)\\mongo.log`", `"ipv6`":true, `"logappend`":true, `"nojournal`":true}}"
} elseif ($configuration -eq "replica_set") {
    $url = "http://localhost:8889/rs"
    $request_body="{$AUTH_PARAMS $SSL_PARAMS `"id`": `"repl0`", `"members`":[{`"rsParams`":{`"priority`": 99}, `"procParams`": {$TEST_PARAMS `"dbpath`":`"$($DATAPATH)\\db27017`", `"port`": 27017, `"logpath`":`"$($LOGPATH)\\db27017.log`", `"nojournal`":false, `"nohttpinterface`": true, `"noprealloc`":true, `"smallfiles`":true, `"nssize`":1, `"oplogSize`": 150, `"ipv6`": true}}, {`"rsParams`": {`"priority`": 1.1}, `"procParams`":{$TEST_PARAMS `"dbpath`":`"$($DATAPATH)\\db27018`", `"port`": 27018, `"logpath`":`"$($LOGPATH)\\db27018.log`", `"nojournal`":false, `"nohttpinterface`": true, `"noprealloc`":true, `"smallfiles`":true, `"nssize`":1, `"oplogSize`": 150, `"ipv6`": true}}, {`"procParams`":{`"dbpath`":`"$($DATAPATH)\\db27019`", `"port`": 27019, `"logpath`":`"$($LOGPATH)\\27019.log`", `"nojournal`":false, `"nohttpinterface`": true, `"noprealloc`":true, `"smallfiles`":true, `"nssize`":1, `"oplogSize`": 150, `"ipv6`": true}}]}" 
} elseif ($configuration -eq "sharded") {
    $url = "http://127.0.0.1:8889/sh"
    $request_body = "{$AUTH_PARAMS $SSL_PARAMS `"routers`": [{$TEST_PARAMS `"port`": 27017, `"logpath`": `"$LOGPATH\\router27017.log`"}, {$TEST_PARAMS `"port`": 27018, `"logpath`": `"$LOGPATH\\router27018.log`"}], `"configsvrs`": [{`"port`": 27016, `"dbpath`": `"$DATAPATH\\db27016`", `"logpath`": `"$LOGPATH\\configsvr27016.log`"}], `"id`": `"shard_cluster_1`", `"members`": [{`"id`": `"sh01`", `"shardParams`": {`"procParams`": {$TEST_PARAMS `"port`": 27020, `"dbpath`": `"$DATAPATH\\db27020`", `"logpath`":`"$LOGPATH\\db27020.log`", `"ipv6`":true, `"logappend`":true, `"nojournal`":false}}}]}" 
} else{
    echo "Unrecognized configuration: $configuration"
    exit 1
}
echo "Sending $request_body to $url"
$http_request.open('POST', $url, $false)
$http_request.setRequestHeader("Content-Type", "application/json")
$http_request.setRequestHeader("Accept", "application/json")
$http_request.send($request_body)
$response = $http_request.statusText
echo $response

# if [ "$2" == "single_server" ]; then
#   echo curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"name\": \"mongod\", \"procParams\": {$TEST_PARAMS \"port\": 27017, \"dbpath\": \"$DATAPATH\", \"logpath\":\"$LOGPATH/mongo.log\", \"ipv6\":true, \"logappend\":true, \"nojournal\":false}}" http://localhost:8889/hosts
#   curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"name\": \"mongod\", \"procParams\": { $TEST_PARAMS \"port\": 27017, \"dbpath\": \"$DATAPATH\", \"logpath\":\"$LOGPATH/mongo.log\", \"ipv6\":true, \"logappend\":true, \"nojournal\":false}}" http://localhost:8889/hosts
#   echo curl -i -H "Accept: application/json" -X GET http://localhost:8889/hosts
#   curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/hosts

# elif [ "$2" == "replica_set" ]; then
  
#   echo curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"id\": \"repl0\", \"members\":[{\"rsParams\":{\"priority\": 99}, \"procParams\": {$TEST_PARAMS \"dbpath\":\"$DATAPATH/db27017\", \"port\": 27017, \"logpath\":\"$LOGPATH/\
# db27017.log\", \"nojournal\":false, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, {\"rsParams\": {\"priority\": 1.1}, \"procParams\":{$TEST_PARAMS \"dbpath\":\
# \"$DATAPATH/db27018\", \"port\": 27018, \"logpath\":\"$LOGPATH/db27018.log\", \"nojournal\":false, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, \
# {\"procParams\":{$TEST_PARAMS \"dbpath\":\"$DATAPATH/db27019\", \"port\": 27019, \"logpath\":\"$LOGPATH/27019.log\", \"nojournal\":false, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}]}" http://localhost:8889/rs
#   curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"id\": \"repl0\", \"members\":[{\"rsParams\":{\"priority\": 99}, \"procParams\": {$TEST_PARAMS \"dbpath\":\"$DATAPATH/db27017\", \"port\": 27017, \"logpath\":\"$LOGPATH/db270\
# 17.log\", \"nojournal\":false, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, {\"rsParams\": {\"priority\": 1.1}, \"procParams\":{$TEST_PARAMS \"dbpath\":\"$DA\
# TAPATH/db27018\", \"port\": 27018, \"logpath\":\"$LOGPATH/db27018.log\", \"nojournal\":false, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}, {\"pr\
# ocParams\":{\"dbpath\":\"$DATAPATH/db27019\", \"port\": 27019, \"logpath\":\"$LOGPATH/27019.log\", \"nojournal\":false, \"nohttpinterface\": true, \"noprealloc\":true, \"smallfiles\":true, \"nssize\":1, \"oplogSize\": 150, \"ipv6\": true}}]}" http://localhost:8889/rs
#   echo curl -i -H "Accept: application/json" -X GET http://localhost:8889/rs/repl0/primary
#   curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/rs/repl0/primary

# elif [ "$2" == "sharded" ]; then
#   echo curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"routers\": [{$TEST_PARAMS \"port\": 27017, \"logpath\": \"$LOGPATH/router27017.log\"}, {$TEST_PARAMS \"port\": 27018, \"logpath\": \"$LOGPATH/router27018.log\"}], \"configsvrs\": [{\"port\": 27016, \"dbpath\": \"$DATAPATH/db27016\", \"logpath\": \"$LOGPATH/configsvr27016.log\"}], \"id\": \"shard_cluster_1\", \"members\": [{\"id\": \"sh01\", \"shardParams\": {\"procParams\": {$TEST_PARAMS \"port\": 27020, \"dbpath\": \"$DATAPATH/db27020\", \"logpath\":\"$LOGPATH/db27020.log\", \"ipv6\":true, \"logappend\":true, \"nojournal\":false}}}]}" http://127.0.0.1:8889/sh
#   curl -i -H "Accept: application/json" -X POST -d "{$AUTH_PARAMS $SSL_PARAMS \"routers\": [{$TEST_PARAMS \"port\": 27017, \"logpath\": \"$LOGPATH/router27017.log\"}, {$TEST_PARAMS \"port\": 27018, \"logpath\": \"$LOGPATH/router27018.log\"}], \"configsvrs\": [{\"port\": 27016, \"dbpath\": \"$DATAPATH/db27016\", \"logpath\": \"$LOGPATH/configsvr27016.log\"}], \"id\": \"shard_cluster_1\", \"members\": [{\"id\": \"sh01\", \"shardParams\": {\"procParams\": {$TEST_PARAMS \"port\": 27020, \"dbpath\": \"$DATAPATH/db27020\", \"logpath\":\"$LOGPATH/db27020.log\", \"ipv6\":true, \"logappend\":true, \"nojournal\":false}}}]}" http://127.0.0.1:8889/sh
#   echo curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/sh/shard_cluster_1
#   curl -f -i -H "Accept: application/json" -X GET http://localhost:8889/sh/shard_cluster_1

# fi
