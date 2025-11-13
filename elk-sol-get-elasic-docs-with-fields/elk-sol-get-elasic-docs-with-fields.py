#Description: This script is used to identify virtual machines which have not been properly tagged in vCenter
#!usr/bin/env python3

# import the Elasticsearch low-level client library
from elasticsearch import Elasticsearch, exceptions
import json
import logging

logging.basicConfig(level=logging.INFO)
es = Elasticsearch(['<your-elastic:port>'])
query_body = {

  "size": 0,
  "query": {
    "bool": {
      "should": [
        { "bool": { "must_not": { "exists": { "field": "tag1.keyword" } } } },
        { "bool": { "must_not": { "exists": { "field": "tag2.keyword" } } } },
        { "bool": { "must_not": { "exists": { "field": "tag3.keyword" } } } },
        { "bool": { "must_not": { "exists": { "field": "tag4.keyword" } } } }
      ],
      "minimum_should_match": 1,
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-30m",
              "lt": "now"
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "<field>": {
      "terms": {
        "field": "<field>",
        "order": {
          "<field>": "desc"
        },
        "size": 100
      },
      "aggs": {
        "<field>": {
          "cardinality": {
            "field": "<field>"
           }
         }
       }
     }
   }
 }


result = es.search(index="<index>", body=query_body)
vm = result["aggregations"]["<field>"]["buckets"]
