# Deploy to DockerHub
VERSION=$(cat VERSION)
docker build -t bbvalabs/deeptracy-api:$VERSION -t bbvalabs/deeptracy-api:latest .
docker login -u $DOCKER_USER -p $DOCKER_PASS
docker push bbvalabs/deeptracy-api:$VERSION
docker push bbvalabs/deeptracy-api:latest
