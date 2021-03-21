from joblib import load

class MachineStatusDetector():
    def load(self):
        self.clf = load('handling-specialty-machine-status-detection.joblib')

    def detect(self, data):
        result = self.clf.predict([data])
        print(result)