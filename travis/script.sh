#!/usr/bin/env bash
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
echo $TRAVIS_BRANCH
tox
docker-compose --version
docker-compose -f tests/acceptance/docker-compose.yml up -d --build
sleep 10
behave --tags=-local tests/acceptance/features
docker-compose -f tests/acceptance/docker-compose.yml kill
docker-compose -f tests/acceptance/docker-compose.yml rm -f
