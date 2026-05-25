from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
from airflow.providers.smtp.hooks.smtp import SmtpHook
import csv, os, io

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
    'start_date': datetime(2026, 3, 4),
    'on_failure_callback': failure_alert
    }

with DAG('load_and_clear_csv',
    default_args=defaults,
    description='Load dirty CSV to Postgres Staging and then clearing data',
    schedule='* * * * *',
    max_active_runs=1,
    catchup=False) as dag:

    file_path = '/opt/airflow/dags/log/bad_data.csv'

    task1 = FileSensor(
        task_id='wait_for_csv',
        filepath=file_path,
        poke_interval=30,
        mode='reschedule'
        )

    def smart_translit(text, idx, full_name_idx):

        if not text or idx != full_name_idx:
            return text
        name = text.strip().lower()

        exceptions = {'igor': 'игорь', 'oleg': 'олег', 'dmitry': 'дмитрий', 'dmitriy': 'дмитрий', 'yuri': 'юрий',
        'artem': 'артём', 'yuriy': 'юрий', 'andrey': 'андрей', 'sergey': 'сергей', 'valeriy': 'валерий',
        'yulia': 'юля', 'daria': 'дарья', 'ulyana': 'ульяна', 'anatoliy': 'анатолий', 'vladimir': 'владимир',
        'lyubov': 'любовь', 'pavel': 'павел', 'victor': 'виктор'
        }

        black_list = ['broken', 'unknown', '\n', '\t']

        for x in black_list:
            if x in name:
                return None

        if name in exceptions:
            return exceptions[name]

        rules = [('shch', 'щ'),
            ('yo', 'ё'), ('zh', 'ж'), ('cz', 'ц'), ('ts', 'ц'), ('ch', 'ч'),
            ('sh', 'ш'), ('ye', 'е'), ('yu', 'ю'), ('ya', 'я'), ('iy', 'ий'),
            ('ij', 'ий'), ('ay', 'ай'), ('uy', 'уй'), ('ey', 'ей'), ('oy', 'ой'),
            ("''", 'ъ'), ("'", 'ь'),
            ('a', 'а'), ('b', 'б'), ('v', 'в'), ('g', 'г'), ('d', 'д'), ('e', 'е'),
            ('z', 'з'), ('i', 'и'), ('j', 'й'), ('k', 'к'), ('l', 'л'), ('m', 'м'),
            ('n', 'н'), ('o', 'о'), ('p', 'п'), ('r', 'р'), ('s', 'с'), ('t', 'т'),
            ('u', 'у'), ('f', 'ф'), ('h', 'х'), ('y', 'ы')
        ]

        res = name
        for lat, cyr in rules:
            res = res.replace(lat, cyr)

        if res.startswith('ы'):
            vowels = 'аеиоуэюя'
            if len(res) > 1 and res[1] in vowels:
                res = 'я' + res[1:]
            else:
                res = 'и' + res[1:]

        return res

    def csv_to_postgres():
        pg_hook = PostgresHook(postgres_conn_id='postgres_conn')

        with open(file_path, 'r', encoding='cp1251', errors='ignore') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')

            try:
                header = [h.strip() for h in next(reader) if h]
                print('header DEBUG:', header)
            except StopIteration:
                print('Файл пуст!')
                return

            # РАЗВЕДКА: ищем максимум колонок в данных
            max_cols_in_data = len(header)
            for row in reader:
                if len(row) > max_cols_in_data:
                    max_cols_in_data = len(row)
            print('max_cols DEBUG: найдено колонок, ', max_cols_in_data)

            full_header = list(header)
            full_name_idx = full_header.index('full_name')

            while len(full_header) < max_cols_in_data:
                full_header.append(f"extra_col_{len(full_header) + 1}")
            full_header.append('full_name_raw')
            print('full_header DEBUG:', full_header)

            quoted_header_list = [f'"{h}"' for h in full_header]
            ddl_cols = ", ".join([f"{h} TEXT" for h in quoted_header_list])
            pg_hook.run(f"DROP TABLE IF EXISTS public.data_raw; CREATE TABLE public.data_raw ({ddl_cols});")

            file.seek(0)
            next(reader) # Скип заголовка

            quoted_header_string = ", ".join(quoted_header_list)
            buffer = io.StringIO()

            conn = pg_hook.get_conn()
            try:
                with conn.cursor() as cur:
                    for i, row in enumerate(reader):
                        clean_row = [smart_translit(row[idx], idx, full_name_idx) if idx < len(row) else None for idx in range(len(full_header)-1)]
                        print('clean_row DEBUG:', clean_row)
                        clean_row.append(row[full_name_idx] if clean_row[full_name_idx] is not None else None)
                        print('clean_row NEW DEBUG:', clean_row)

                        csv.writer(buffer, delimiter=';').writerow(clean_row)

                        if (i + 1) % 100000 == 0:
                            buffer.seek(0)
                            cur.copy_expert(f"COPY public.data_raw ({quoted_header_string}) FROM STDIN WITH (FORMAT csv, DELIMITER ';')", buffer)
                            print(f"DEBUG: Загружено {i + 1} строк...")
                            buffer = io.StringIO()

                    # Догружаем остаток
                    buffer.seek(0)
                    if buffer.getvalue():
                        cur.copy_expert(f"COPY public.data_raw ({quoted_header_string}) FROM STDIN WITH (FORMAT csv, DELIMITER ';')", buffer)

                    conn.commit()
                    print(f"DEBUG: Всего успешно загружено {i + 1} строк.")
            finally:
                conn.close()

    task2 = PythonOperator(
        task_id='csv_to_postgres',
        python_callable=csv_to_postgres
    )

    task3 = SQLExecuteQueryOperator(
        task_id='staging_to_target',
        conn_id='postgres_conn',
        sql='''drop table if exists public.stage;
        create temp table stage as
        select
            id::int
            , NULLIF(TRIM(initcap(regexp_replace(
                full_name, '(\s?супер\s?|.*длинный.текст.который.сломает.*)|[^a-zA-Zа-яА-ЯёЁ\s-]', '', 'g'
            ))), '')::varchar(30) full_name
            , case when amount ~ '^[0-9]+([.,][0-9]+)?$' then round(replace(amount, ',', '.')::decimal, 2) else 0 end amount
            , case when pg_input_is_valid(created_at, 'date') then to_char(created_at::date, 'YYYY-MM-DD')::date else null end as created_at
            , case when email ~ '^(.+)@(.+)\.(.+)$' then email::varchar(30) else null end email
            , nullif(concat_ws(' ', comment, to_jsonb(t.*) ->> 'extra_col_7'), '') comment
        from public.data_raw t
        where id is not null and not (full_name is null and email is null);

        with inserted as (
            -- Кладём причёсанные данные в целевую таблицу
            insert into public.data select * from stage
            on conflict (id) do nothing
            returning id
        ),
        stats as (
        -- Отчёт об обработанных данных
            SELECT
                COUNT(*) as total_received -- Общее кол-во строк в файле
                , (SELECT COUNT(*) FROM stage) as valid_rows -- Сколько прошли фильтры
                , (SELECT COUNT(*) FROM inserted) as actual_inserts -- Сколько вставлено (новых)
                , (SELECT COUNT(*) FROM stage) - (SELECT COUNT(*) FROM inserted) as duplicates_skipped -- Пропущенные дубли
                , COUNT(*) - (SELECT COUNT(*) FROM stage) as rows_deleted -- Сколько строк НЕ попало в stage (удалено)
                , (SELECT COUNT(*)
                 FROM information_schema.columns
                 WHERE table_name = 'data_raw' AND column_name LIKE 'extra_col_%'
                ) as extra_cols_count -- Количество экстра-колонок
                , SUM(CASE WHEN r.full_name_raw <> s.full_name THEN 1 ELSE 0 END) as changed_names -- Обработанные имена
                , SUM(CASE WHEN r.created_at::text IS DISTINCT FROM s.created_at::text THEN 1 ELSE 0 END) as changed_or_deleted_dates -- Обработанные даты
                , SUM(CASE WHEN r.amount::text IS DISTINCT FROM s.amount::text THEN 1 ELSE 0 END) as changed_amounts -- Обработанные amount
                , SUM(CASE WHEN r.email IS DISTINCT FROM s.email THEN 1 ELSE 0 END) as changed_emails -- Обработанные email
                , SUM(CASE WHEN (to_jsonb(r.*) ->> 'extra_col_7') IS NOT NULL -- Количество конкатенаций (считаем заполненные экстра-поля через JSON, чтобы не упасть)
                          AND (to_jsonb(r.*) ->> 'extra_col_7') <> '' THEN 1 ELSE 0 END) as concatenations_done
                , now() as report_time -- Время отчёта
            FROM public.data_raw r
            LEFT JOIN stage s ON r.id::text = s.id::text -- используем LEFT JOIN, чтобы видеть удаленные
        )
        insert into public.report select * from stats''',
        on_success_callback=lambda _: os.remove(file_path)
        )

    task1 >> task2 >> task3
