from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.mongo_hook import MongoHook
import logging
from datetime import datetime


def get_mongodb_connection():
    conn = MongoHook(conn_id='playrecipe_mongo').get_conn()
    return conn


def extract(collection_name):
    collection = get_mongodb_connection().get_database('playrecipe').get_collection(collection_name)
    logging.info("Extract started")
    pipeline = [{"$unwind": "$playlists"}, {"$unwind": "$playlists.tracks"},
                {"$group": {"_id": {"id": "$playlists.tracks.id", "name": "$playlists.tracks.name",
                                    "artists": "$playlists.tracks.artists.name"}, "total": {"$sum": 1}}},
                {"$project": {"_id": 0, "name": "$_id.name", 'artists': '$_id.artists', "total": 1}},
                {"$sort": {"total": -1, "name": 1}}, {"$limit": 50}]
    results = collection.aggregate(pipeline=pipeline)
    logging.info("Extract done")
    return results


def transform(docs):
    logging.info("Transform started")
    transformed = [doc for doc in docs]
    logging.info("Transform done")
    return transformed


def load(docs,collection_name):
    collection = get_mongodb_connection().get_database('playrecipe').get_collection(collection_name)
    logging.info("Load started")
    before = collection.count_documents({})
    logging.info('before insert', before)
    collection.insert_many(docs)
    after = collection.count_documents({})
    logging.info(after, 'documents inserted')
    logging.info('Load stopped')


def etl():
    # execution_date = context['execution_date']
    # task_instance = context['task_instance']
    logging.info('ETL started')
    extracted = extract('playlist')
    transformed = transform(extracted)
    load(transformed,'mostchoicetracks')
    logging.info('etl done')


mostchioce = DAG(
    dag_id='most_chioce',
    start_date=datetime(2020, 9, 1),
    schedule_interval='@daily',
    catchup=False
)

task = PythonOperator(
    task_id='most_choice_tracks',
    python_callable=etl,
#     provide_context=True,
    dag=mostchioce
)
