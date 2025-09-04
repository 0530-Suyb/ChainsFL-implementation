Fabric 2.2.14 can start up normally, but I am not sure if Fabric 2.1 can (start up too).
Try it

```
cd test-network

# start up network and install chaincode
oneStep.sh

# stop network
./network.sh down
```

Remeber modifying environment variable "FabricL" in interRun.sh
