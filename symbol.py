class Symbol:
    max_index = 0

    @classmethod
    def next_index(cls):
        cls.max_index = cls.max_index+1
        return cls.max_index

    def __init__(self, series, id=None, symbol_shift=0, label=None):
        self.series = series
        self.id = id or self.__class__.next_index()
        self.symbol_shift = symbol_shift
        self.label = label

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
        
    def match(self, id):
        return True if id == self.id else False
        
class ListOfLostSymbol(Symbol):
    
    def __init__(self, series, id=None, symbol_shift=0, list_of_lost=[], label=None):
        self.series = series
        self.id = id or self.__class__.next_index()
        self.symbol_shift = symbol_shift
        self.list_of_lost = list_of_lost #list of identifiers of symbols this symbol replaced
        self.label=label
        
    def swallow(self, symbol):
        """swallows other symbol. Puts its identifier and list of lost identifiers to his list of lost identifiers"""
        self.list_of_lost.append(symbol.id)
        if 'list_of_lost' in dir(symbol):
            self.list_of_lost = self.list_of_lost + symbol.list_of_lost
            
    def match(self, id):
        return True if id == self.id or id in self.list_of_lost else False
    
