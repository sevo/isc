class DistanceMatrix:
    def __init__(self, distance_operator):
        self.distances = {}
        self.distance_operator = distance_operator

    def size(self):
        return len(self.distances)

    def symbols(self):
        return self.distances.keys()

    def add(self, symbol):
        new_distances = {symbol: 0.0}
        for other_symbol in self.distances.keys():
            new_distances[other_symbol] = self.distance_operator.distance(symbol.series, other_symbol.series)
        self.distances[symbol] = new_distances

    def distance(self, a, b):
        if (a in self.distances and b in self.distances[a]):
            return self.distances[a][b]
        elif (b in self.distances and a in self.distances[b]):
            return self.distances[b][a]
        else:
            return None


