from influxdb import InfluxDBClient
from dateutil.parser import parse

influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')
query = 'SELECT time, value FROM watering WHERE value = \'rpi\' ORDER BY time DESC LIMIT 1'
result = next(influx_client.query(query).get_points())
time = parse(result['time'])

print(int(time.timestamp() * 1e9))
