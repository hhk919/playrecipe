from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.mongo_hook import MongoHook
import logging
from datetime import datetime

def get_mongo_connection():
    hook = MongoHook(conn_id='playrecipe_mongo')
    return hook.get_collection(mongo_collection='playlists',mongo_db='playrecipe')

def extract() :
    logging.info("Extract started")
    pipeline = [{"$unwind": "$playlists"}, {"$unwind": "$playlists.tracks"},
                {"$group": {"_id": {"id": "$playlists.tracks.id", "name": "$playlists.tracks.name",
                                    "artists": "$playlists.tracks.artists.name"}, "total": {"$sum": 1}}},
                {"$project": {"_id": 0, "name": "$_id.name", 'artists': '$_id.artists', "total": 1}},
                {"$sort": {"total": -1, "name": 1}}, {"$limit": 50}]
    cursor = get_mongo_connection().aggregate(pipeline=pipeline)
    logging.info("Extract done")
    result = list(cursor)
    return result

def transform(extracted) :
    logging.info("Transform started")
    transformed = extracted
    logging.info("Transform done")
    return transformed

def load(transformed) :
    logging.info("Load started")
    documents = transformed
    conn = get_mongo_connection()
    before = conn.count_documents({})
    logging.info('before insert',before)
    get_mongo_connection().insert_many(documents)
    after = conn.count_documents({})
    logging.info(after,'documents inserted')
    logging.info('Load stopped')

def etl(**context) :
    execution_date = context['execution_date']
    # task_instance = context['task_instance']
    logging.info(execution_date,'ETL started')
    extracted = extract()
    transformed = transform(extracted)
    load(transformed)
    logging.info('etl done')

mostchioce = DAG(
    dag_id = 'most_chioce',
    start_date = datetime(2020,9,1),
    schedule_interval = '@daily',
    catchup = False
)

task = PythonOperator(
    task_id = 'most_choice_tracks',
    python_callable = etl,
    provide_context = True,
    dag = mostchioce
)
