from influxdb import InfluxDBClient

influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')
query = 'SELECT value FROM moisture ORDER BY time DESC LIMIT 1'
result = next(influx_client.query(query).get_points())
print(result['value'])
