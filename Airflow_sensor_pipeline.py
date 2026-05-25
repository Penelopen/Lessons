from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
from airflow.providers.smtp.hooks.smtp import SmtpHook
import os

def failure_alert(context):
    target_email=BaseHook.get_connection('smtp_conn').description
    if not target_email:
        print("Ошибка: Поле Description в Connection 'smtp_conn' пустое!")
        return

    hook = SmtpHook(smtp_conn_id='smtp_conn')
    with hook.get_conn() as smtp_client:  # noqa: F841
        hook.send_email_smtp(
            to=target_email,
            subject=f"🚨 Airflow Alert: {context['task_instance'].dag_id}.{context['task_instance'].task_id} Failed",
            html_content = f"""
            <h3>Таска <b>{context['task_instance'].task_id}</b> в даге {context['task_instance'].dag_id} упала!</h3>
            <p><b>Ошибка:</b> <pre style="color:red;">{context.get('exception')}</pre></p>
            <p><a href="{context['task_instance'].log_url}">Посмотреть логи в интерфейсе</a></p>
            """)

defaults = {'owner': 'TonyB',
    'start_date': datetime(2026, 2, 25),
    'on_failure_callback': failure_alert}

with DAG ('weather_to_csv_to_postgres',
    default_args=defaults,
    description='Get weather from API and put to CSV. After that CSV load to Postgres',
    schedule='* * * * *',
    max_active_runs=1,
    catchup=False
    ) as dag:

    task1 = FileSensor(
        task_id='wait_for_csv',
        filepath='/opt/airflow/dags/log/weather.csv',
        poke_interval=30,
##        mode='reschedule'
    )

    def csv_to_postgres():
        pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
        pg_hook.run("TRUNCATE public.weather_raw")
        pg_hook.copy_expert("COPY public.weather_raw FROM STDIN WITH (DELIMITER ',')", '/opt/airflow/dags/log/weather.csv')
        os.remove('/opt/airflow/dags/log/weather.csv')

    task2 = PythonOperator(
        task_id='csv_to_postgres',
        python_callable=csv_to_postgres
    )

    task3 = SQLExecuteQueryOperator(
        task_id='raw_to_final',
        conn_id='postgres_conn',
        sql='INSERT INTO public.weather (datetime, city, value, measure) SELECT datetime::timestamp, city::varchar(30), value::decimal, measure::char(1) FROM public.weather_raw'
    )

    task1 >> task2 >> task3