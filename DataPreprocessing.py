import csv
import math

class DataPreprocessing():
    def __init__(self, db):
        self.db = db
        self.faulty_data_timeframe = {
            'motorfan': {
                'start': '2021-02-18 11:33:00',
                'end'  : '2021-02-18 12:00:59'
            }
        }

    def run(self):
        healthy_data_index = [
            {
                'location': 'motorfan',
                'sensor_id': '00:13:A2:00:41:A8:5A:7C',
                'start': '2020-10-27 12:35:00',
                'end': '2020-10-27 12:57:59'
            },
            {
                'location': 'motorfan',
                'sensor_id': '00:13:A2:00:41:A8:60:87',
                'start': '2020-11-12 12:07:00',
                'end': '2020-11-12 12:36:59'
            },
            {
                'location': 'lowerbrace',
                'sensor_id': '00:13:A2:00:41:A8:60:87',
                'start': '2020-11-24 15:37:00',
                'end': '2020-11-24 15:59:59'
             },
            {
                'location': 'upperrockerarm',
                'sensor_id': '00:13:A2:00:41:A8:60:87',
                'start': '2020-11-24 12:53:00',
                'end': '2020-11-24 13:17:59'
            }
        ]

        faulty_data_index = [
            {
                'location': 'motorfan',
                'sensor_id': '00:13:A2:00:41:A8:5C:3A',
                'start': '2021-02-12 12:04:00',
                'end': '2021-02-12 12:29:59'
            },
            {
                'location': 'motorfan',
                'sensor_id': '00:13:A2:00:41:A8:60:87',
                'start': '2021-02-18 11:33:00',
                'end': '2021-02-18 12:00:59'
            },
            {
                'location': 'lowerbrace',
                'sensor_id': '00:13:A2:00:41:A8:5C:3A',
                'start': '2021-02-10 11:12:00',
                'end': '2021-02-10 11:38:59'
            },
            {
                'location': 'lowerbrace',
                'sensor_id': '00:13:A2:00:41:A8:60:87',
                'start': '2021-02-18 12:10:00',
                'end': '2021-02-18 12:35:59'
            },
            {
                'location': 'upperrockerarm',
                'sensor_id': '00:13:A2:00:41:A8:5C:3A',
                'start': '2021-02-10 12:14:00',
                'end': '2021-02-10 12:40:59'
            },
            {
                'location': 'upperrockerarm',
                'sensor_id': '00:13:A2:00:41:A8:60:87',
                'start': '2021-02-18 12:54:00',
                'end': '2021-02-18 13:19:59'
            }
        ]

        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['location', 'rms_y', 'average', 'standard deviation', 'variance'])
            for d in faulty_data_index:
                query = 'select * from faulty_data where'
                query += ' sensor_id=\'' + d['sensor_id'] + '\' and'
                query += ' location=\'' + d['location'] + '\' and'
                query += ' sensed_time > \'' + d['start'] + '\' and'
                query += ' sensed_time < \'' + d['end'] + '\''
                result = self.execute(query)
                self.write_csv(result, writer, 1)

            for d in healthy_data_index:
                query = 'select * from healthy_data where'
                query += ' sensor_id=\'' + d['sensor_id'] + '\' and'
                query += ' location=\'' + d['location'] + '\' and'
                query += ' sensed_time > \'' + d['start'] + '\' and'
                query += ' sensed_time < \'' + d['end'] + '\''
                result = self.execute(query)
                self.write_csv(result, writer, 0)

    def execute(self, query):
        return self.db.read(query)

    def write_csv(self, result, writer, status):
        data_queue = []
        for row in result:
            loc = row[15]
            time = row[2]
            rms_y = row[4]

            if len(data_queue) <= 10:
                data_queue.append(rms_y)
            else:
                data_queue.pop(0)
                data_queue.append(rms_y)
                avg, sd, var = self.calculate_feature(data_queue)
                writer.writerow([loc, rms_y, avg, sd, var, status])

    def calculate_feature(self, data):
        sum = 0
        size = len(data)
        for d in data:
            sum += d
        avg = sum / size

        sum = 0
        for d in data:
            sum += (d - avg) ** 2
        var = sum / size

        sd = math.sqrt(var)

        return avg, var, sd

        '''
        mysql> desc  sensor_data;
        +---------------+-------------+------+-----+---------+-------+
        | Field         | Type        | Null | Key | Default | Extra |
        +---------------+-------------+------+-----+---------+-------+
        | gateway_id    | varchar(50) | YES  |     | NULL    |       |
        | sensor_id     | varchar(50) | YES  |     | NULL    |       |
        | sensed_time   | datetime    | YES  |     | NULL    |       |
        | rms_x         | float       | YES  |     | NULL    |       |
        | rms_y         | float       | YES  |     | NULL    |       |
        | rms_z         | float       | YES  |     | NULL    |       |
        | max_x         | float       | YES  |     | NULL    |       |
        | max_y         | float       | YES  |     | NULL    |       |
        | max_z         | float       | YES  |     | NULL    |       |
        | min_x         | float       | YES  |     | NULL    |       |
        | min_y         | float       | YES  |     | NULL    |       |
        | min_z         | float       | YES  |     | NULL    |       |
        | battery_level | float       | YES  |     | NULL    |       |
        | rssi          | int(11)     | YES  |     | NULL    |       |
        | temperature   | int(11)     | YES  |     | NULL    |       |
        +---------------+-------------+------+-----+---------+-------+
        
        mysql> desc healthy_data;
        +---------------+-------------+------+-----+---------+-------+
        | Field         | Type        | Null | Key | Default | Extra |
        +---------------+-------------+------+-----+---------+-------+
    0   | gateway_id    | varchar(50) | YES  |     | NULL    |       |
    1   | sensor_id     | varchar(50) | YES  |     | NULL    |       |
    2   | sensed_time   | datetime    | YES  |     | NULL    |       |
    3   | rms_x         | float       | YES  |     | NULL    |       |
    4   | rms_y         | float       | YES  |     | NULL    |       |
    5   | rms_z         | float       | YES  |     | NULL    |       |
    6   | max_x         | float       | YES  |     | NULL    |       |
    7   | max_y         | float       | YES  |     | NULL    |       |
    8   | max_z         | float       | YES  |     | NULL    |       |
    9   | min_x         | float       | YES  |     | NULL    |       |
    10  | min_y         | float       | YES  |     | NULL    |       |
    11  | min_z         | float       | YES  |     | NULL    |       |
    12  | battery_level | float       | YES  |     | NULL    |       |
    13  | rssi          | int(11)     | YES  |     | NULL    |       |
    14  | temperature   | int(11)     | YES  |     | NULL    |       |
    15  | location      | varchar(40) | YES  |     | NULL    |       |
        +---------------+-------------+------+-----+---------+-------+
        
        mysql> desc faulty_data;
        +---------------+-------------+------+-----+---------+-------+
        | Field         | Type        | Null | Key | Default | Extra |
        +---------------+-------------+------+-----+---------+-------+
     0  | gateway_id    | varchar(50) | YES  |     | NULL    |       |
     1  | sensor_id     | varchar(50) | YES  |     | NULL    |       |
     2  | sensed_time   | datetime    | YES  |     | NULL    |       |
     3  | rms_x         | float       | YES  |     | NULL    |       |
     4  | rms_y         | float       | YES  |     | NULL    |       |
     5  | rms_z         | float       | YES  |     | NULL    |       |
     6  | max_x         | float       | YES  |     | NULL    |       |
     7  | max_y         | float       | YES  |     | NULL    |       |
     8  | max_z         | float       | YES  |     | NULL    |       |
     9  | min_x         | float       | YES  |     | NULL    |       |
     10 | min_y         | float       | YES  |     | NULL    |       |
     11 | min_z         | float       | YES  |     | NULL    |       |
     12 | battery_level | float       | YES  |     | NULL    |       |
     13 | rssi          | int(11)     | YES  |     | NULL    |       |
     14 | temperature   | int(11)     | YES  |     | NULL    |       |
     15 | location      | varchar(50) | YES  |     | NULL    |       |
        +---------------+-------------+------+-----+---------+-------+
        '''