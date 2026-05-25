from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.smtp.hooks.smtp import SmtpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
import re

defaults = {'owner': 'TonyB'
}

with DAG ('airflow_test',
default_args=defaults,
start_date=datetime(2023, 12, 29),
max_active_runs=1,
description='Super Mega Sexy Challenge',
schedule='@hourly',
catchup=True
) as dag:

    def my_process_function(ti, **context):
        ds = context['ds']
        gp_hook = PostgresHook(postgres_conn_id='greenplum_conn')
        pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
        existed_data = pg_hook.get_records(f"SELECT id from numbers WHERE date = '{ds}'")
        existed_ids = tuple(x[0] for x in existed_data) if existed_data else (0, 0)
        data = gp_hook.get_records(f"SELECT id, number, title, date FROM numbers WHERE date = '{ds}' and id not in {existed_ids} LIMIT 10000")
        processed = []
        for id, number, title, date in data:
            new_number = re.sub(r'^(\w)(\d{3})(\w{2})(\d+)$', r'\4\3\2\1', number)
            processed.append((id, number + ' ' + new_number, title.upper(), date))
        print(context)
        pg_hook.insert_rows(table='numbers', rows=processed)

        ti.xcom_push(key='rows_cnt', value=len(processed))

    gp_to_pg = PythonOperator(task_id='gp_to_pg', python_callable=my_process_function)

    def send_email(ti):
        rows_cnt = ti.xcom_pull(task_ids='gp_to_pg', key='rows_cnt')
        hook = SmtpHook(smtp_conn_id='smtp_conn')
        with hook.get_conn() as smtp_client:
            hook.send_email_smtp(
                to='7029293@gmail.com',
                subject='Ищкере',
                html_content=f'{rows_cnt} строк уехали в Postgres 🚀'
            )

    success_email = PythonOperator(
        task_id='success_email',
        python_callable=send_email
    )

    gp_to_pg >> success_email