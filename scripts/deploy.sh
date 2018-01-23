#!/usr/bin/env bash

if [[ ${TRAVIS_TEST_RESULT=0} == 1 ]]; then
  echo "Tests failed !!"
  exit 1;
fi

if [[ $TRAVIS_PULL_REQUEST == "false" ]]; then
  echo "Skipping pull request !!"
  exit 0;
fi

eval "$(ssh-agent -s)" #start the ssh agent
chmod 600 .travis/deploy.key # this key should have push access
ssh-add .travis/deploy.key
ssh-keyscan <your dokku host> >> ~/.ssh/known_hosts
git config --global push.default simple

if [[ $TRAVIS_BRANCH == "master" ]]; then
  git remote add deploy.agendaodonto.com:backend
  git push deploy master:master
  echo "Deploying to Production"
else
  echo "Skipping deploy to production. (Not on master branch)"
fi

if [[ $TRAVIS_BRANCH == "develop" ]]; then
  git remote add deploy.agendaodonto.com:backend-staging
  git push deploy develop:master
  echo "Deploying to Staging"
else
  echo "Skipping deploy to staging. (Not on develop branch)"
fi

