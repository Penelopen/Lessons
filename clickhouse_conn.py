import clickhouse_connect

# Подключение к ClickHouse
def connect_clickhouse():
    try:
        client = clickhouse_connect.get_client(host='192.168.114.131', port=8123, user='default', password='123456')
        print("Connected to ClickHouse")
        version = client.command('SELECT version()')
        print("ClickHouse version:", version)
    except Exception as e:
        print(f"Error connecting to ClickHouse: {e}")

connect_clickhouse()