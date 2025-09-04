./network_normal.sh up createChannel -c mychannel

./network_normal.sh deployCC -ccn mycc -ccp ../cc-demo -ccl go
#./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go -ccl go

#./network.sh deployCC -ccn cc2 -ccp ../cc-demo -ccl go -ccep "OR('Org1MSP.member','Org2MSP.member')"
#./network.sh deployCC -ccn fabcar -ccp ../../caliper-benchmarks/src/fabric/samples/fabcar/go -ccl go

#./network.sh deployCC -ccn cc3 -ccp ../cc-demo -ccl go

#./network.sh deployCC -ccn cc4 -ccp ../cc-demo -ccl go

export FABRIC_CFG_PATH=$PWD/configtx/

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
#export FABRIC_LOGGING_SPEC=DEBUG

#export CORE_PEER_TLS_ENABLED=true
#export CORE_PEER_LOCALMSPID="Org2MSP"
#export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
#export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
#export CORE_PEER_ADDRESS=peer0.org2.example.com:9051

peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n mycc --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" -c '{"function":"set","Args":["a","1"]}'

peer chaincode query -C mychannel -n mycc -c '{"Args":["get","a"]}'
# docker exec cli peer chaincode query -C mychannel -n mycc -c '{"Args":["get","a"]}'


