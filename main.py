from DataPreprocessing import DataPreprocessing
from SensorDB  import SensorDB
from ModelTraining import ModelTraining
from MachineStatusDetector import MachineStatusDetector
import argparse
import sys

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parse command")
    parser.add_argument("-s", "--dbserver", help="DB server", required=True)
    parser.add_argument("-d", "--database", help="database id on DB", required=True)
    parser.add_argument("-u", "--username", help="user id", required=True)
    parser.add_argument("-p", "--password", help="user password", required=True)

    options = parser.parse_args(args)
    return options

if __name__ == '__main__':
    options = getOptions(sys.argv[1:])

    sensorDB = SensorDB()
    sensorDB.connect(options.dbserver, options.database, options.username, options.password)

    processing = DataPreprocessing(sensorDB)
    processing.run()

    model = ModelTraining()
    model.load()
    model.train()
    model.save()

    detector = MachineStatusDetector()
    detector.load()
    data = [1, 0, 0, 100.98, 84.19363636363636, 590.1159504132231, 24.29230228721072]
    detector.detect(data)
