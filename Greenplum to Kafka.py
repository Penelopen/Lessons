import pandas as pd
from sqlalchemy import create_engine
import clickhouse_connect
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='192.168.205.128:9092', acks=1, retries=5)
engine = create_engine('postgresql://gpdb:123456@192.168.205.128:5433/postgres')
##ch_client = clickhouse_connect.get_client(host='192.168.205.128', port=8126, username='default', password='123456')

try:
    print("Читаем данные из Greenplum...")
    result = pd.read_sql("SELECT id, number, title, date::text FROM public.numbers LIMIT 50000", engine)

    if not result.empty:
##        result.to_parquet(r'C:\Users\User\Downloads\numbers.parquet', index=False)
##        print("Файл numbers.parquet создан.")
##        ch_client.insert_df('numbers', result)

        for row in result.to_dict('records'):
            json_bytes = json.dumps(row).encode('utf-8')
            producer.send('numbers', json_bytes)
        print(result)
        producer.flush()
    else:
        print("Таблица пуста.")

except Exception as e:
    print(f"Ошибка: {e}")
