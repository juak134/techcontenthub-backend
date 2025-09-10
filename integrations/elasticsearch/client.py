import os
from elasticsearch import Elasticsearch
def get_es():
    host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    port = os.getenv("ELASTICSEARCH_PORT", "9200")
    return Elasticsearch(f"http://{host}:{port}")
def get_index_name():
    return os.getenv("ELASTICSEARCH_INDEX", "content_metrics")
