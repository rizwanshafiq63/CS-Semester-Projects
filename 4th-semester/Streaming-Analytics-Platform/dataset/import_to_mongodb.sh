#!/bin/bash

# MongoDB Import Script for Streaming Platform
# Generated: 2025-12-03 17:50:04

mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection genres --file genres.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection actors --file actors.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection directors --file directors.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection users --file users.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection movies --file movies.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection ratings --file ratings.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection reviews --file reviews.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection watch_history --file watch_history.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection recommendations --file recommendations.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection subscriptions --file subscriptions.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection payments --file payments.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection devices --file devices.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection transaction_log --file transaction_log.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection resource_locks --file resource_locks.json --jsonArray
mongoimport --uri "mongodb+srv://streaming_admin:adb123@cluster0.36uks1x.mongodb.net/streaming" --collection system_indexes --file system_indexes.json --jsonArray
