from datetime import datetime
import json, os.path

class Storage():
    def __init__(self, loadData=True):
        self.storagePath = 'storage.json'
        self.competitors = {}
        self.scores = {}
        self.arrivals = {}
        self.arrivalsYesterday = {}
        self.lastDate = datetime.now()

        if(loadData):
            self.loadData()

    def loadData(self):
        if(os.path.isfile(self.storagePath)):
            with open(self.storagePath) as dataFile:
                data = json.load(dataFile)

                self.competitors = {}
                for comp in data['competitors'].items():
                   self.competitors[int(comp[0])] = comp[1]

                self.scores = {}
                for score in data['scores'].items():
                   self.scores[int(score[0])] = int(score[1])

                self.arrivals = {}
                for arr in data['arrivals'].items():
                    print(arr[0])
                    self.arrivals[int(arr[0])] = self.decodeDate(arr[1])

                self.arrivalsYesterday = {}
                for arrYest in data['arrivalsYesterday'].items():
                    self.arrivalsYesterday[int(arrYest[0])] = self.decodeDate(arrYest[1])

                self.lastDate = self.decodeDate(data['lastDate'])


    def storeData(self):
        with open(self.storagePath, 'w') as dataFile:
            data = {}
            data['competitors'] = self.competitors
            data['scores'] = self.scores

            data['arrivals'] = {}
            for arr in self.arrivals.items():
                data['arrivals'][arr[0]] = self.encodeDate(arr[1])
            
            data['arrivalsYesterday'] = {}
            for arrYest in self.arrivalsYesterday.items():
                data['arrivalsYesterday'][arrYest[0]] = self.encodeDate(arrYest[1])

            data['lastDate'] = self.encodeDate(self.lastDate)
            json.dump(data, dataFile)

    def decodeDate(self, date):
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    def encodeDate(self, date):
        return date.replace(microsecond=0).isoformat(' ')