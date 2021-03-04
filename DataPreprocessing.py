class DataPreprocessing():
    def __init__(self, db):
        self.db = db
        self.faulty_data_timeframe = {
            'motorfan': {
                'start': '2021-02-18 11:33:00',
                'end'  : '2021-02-18 12:00:59'
            }
        }

    def retrieve(self):
        query = 'select * from sensor_data'

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
        '''
        results = self.db.read(query)
        for item in results:
            sensor_id = item[1]
            rms_y =  item[4]
            print('*** Sensor ID: ' + sensor_id + ', ' + str(rms_y))