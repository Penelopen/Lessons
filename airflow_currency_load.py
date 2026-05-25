from airflow import DAG
from datetime import datetime
import requests
import xml.etree.ElementTree as ET
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

defaults = {'owner': 'TonyB',
    'start_date': datetime(2026, 2, 1),
    'retry_exponential_backoff': True
    }

with DAG('load_cbr_to_postgres',
    default_args=defaults,
    description='My super NEW attempt',
    schedule='@daily',
    max_active_runs=1,
    catchup=True
    ) as dag:

    def get_data(ti, **kwargs):
        processing_date = datetime.strptime(kwargs['ds'], '%Y-%m-%d').strftime('%d/%m/%Y')
        url='https://cbr.ru/scripts/XML_daily.asp?date_req='
        link = url + processing_date
        response = requests.get(link)

        res = []
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            cbr_date = root.get('Date')
            formatted_cbr_date = datetime.strptime(cbr_date, '%d.%m.%Y').strftime('%Y-%m-%d')
            ti.xcom_push(key='cbr_date', value=formatted_cbr_date)
            for valute in root.findall('Valute'):
                v_id = valute.get('ID')
                num_code = valute.find('NumCode').text
                char_code = valute.find('CharCode').text
                name = valute.find('Name').text
                value = valute.find('Value').text.replace(',', '.')
                res.append((v_id, num_code, char_code, name, value, formatted_cbr_date))
        else: raise Exception(f"Ошибка API: {response.status_code}")  # noqa: E701

        return res

    task1 = PythonOperator(
        task_id='get_currency',
        python_callable=get_data
    )

    def put_process(ti, **kwargs):
        date_for_check = ti.xcom_pull(task_ids='get_currency', key='cbr_date')
        pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
        pg_hook.run(f"DELETE FROM public.currency WHERE date = '{date_for_check}'")
        processed = ti.xcom_pull(task_ids='get_currency')
        pg_hook.insert_rows(table='public.currency', rows=processed, target_fields=['valute_id', 'num_code', 'currency', 'title', 'value', 'date'])

    task2 = PythonOperator(
        task_id='put_to_postgres',
        python_callable=put_process
    )

    task1 >> task2