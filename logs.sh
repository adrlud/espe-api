ssh -T espe@144.202.14.56 << EOSSH
cd espe-api/
docker-compose logs | grep "WARNING"
docker-compose logs 
logout

