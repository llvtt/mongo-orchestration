$BASE_PATH="C:\mongo"
$CONFIG_FILE="C:\Users\luke\code\mongo-orchestration\mongo-orchestration.config"
$RELEASE="26-release"
$PYTHON_BIN="C:\Python27\python.exe"



echo "====== CLEANUP ======"
echo "*** Killing any existing MongoDB Processes which may not have shut down on a prior job."
$mongods = (Get-Process mongod)
echo "Found existing mongod Processes: $mongods"
$mongoss = (Get-Process mongos)
echo "Found existing mongos Processes: $mongoss"
Stop-Process -InputObject $mongods
Stop-Process -InputObject $mongoss

$pythons = (Get-Process python)
foreach ($python in $pythons) {
    $procid = $python.id
    $wmi = (Get-WmiObject Win32_Process -Filter "Handle = '$procid'")
    if ($wmi.CommandLine -like "*server.py*") {
	Stop-Process -id $wmi.Handle
    }
}

echo "remove old files from $BASE_PATH"
del -Recurse $BASE_PATH
echo "====== END CLEANUP ======"

echo "Start-Process -FilePath $PYTHON_BIN -ArgumentList server.py,start,-f,$CONFIG_FILE,-e,$RELEASE,--no-fork"
Start-Process -FilePath $PYTHON_BIN -ArgumentList server.py,start,-f,$CONFIG_FILE,-e,$RELEASE,--no-fork
