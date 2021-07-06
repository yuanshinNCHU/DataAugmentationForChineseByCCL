import os

class DataLoader:

    def __init__(self, path):

        self._pictPaths = {}
        files = os.listdir(path)
        for f in files:
            if f[0] not in self._pictPaths:
                self._pictPaths[f[0]] = []
            self._pictPaths[f[0]].append(path + f)
    
    def getData(self):
        return self._pictPaths