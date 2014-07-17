$BASE_PATH="C:\mongo"
$CONFIG_FILE="C:\Users\luke\code\mongo-orchestration\mongo-orchestration.config"
$RELEASE="26-release"
$PYTHON_BIN="C:\Python27\python.exe"



echo "====== CLEANUP ======"
echo "*** Killing any existing MongoDB Processes which may not have shut down on a prior job."
$mongods = (get-process mongod)
echo "Found existing mongod Processes: $mongods"
$mongoss = (get-process mongos)
echo "Found existing mongos Processes: $mongoss"
echo $mongods | stop-process
echo $mongoss | stop-process

$pythons = (get-process python)
echo "Found existing Python Processes: $pythons"
echo $pythons | stop-process

echo "remove old files from $BASE_PATH"
del -Recurse $BASE_PATH
echo "====== END CLEANUP ======"

echo "$PYTHON_BIN server.py start -f $CONFIG_FILE -e $RELEASE --no-fork"
& $PYTHON_BIN server.py start -f $CONFIG_FILE -e $RELEASE --no-fork
