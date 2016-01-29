import abc

class SymbolAlphabet:
    __metaclass__  = abc.ABCMeta
    
    def __init__(self, distance_operator, limit_distance=0.0):
        self.distance_operator = distance_operator
        self.limit_distance = limit_distance

    @abc.abstractmethod
    def size(self):
        """Returns size of the alphabet"""

    @abc.abstractmethod
    def symbols(self):
        """Returns a list of stored symbols"""

    @abc.abstractmethod
    def add(self, symbol):
        """Adds a symbol into the alphabet"""
        raise NotImplementedError

    @abc.abstractmethod
    def distance(self, a, b):
        """Returns distacne between symbols"""
        
    @abc.abstractmethod
    def get_similar(self, normalized, symbol_shift):
        """Returns similar symbol from the alphabet"""
        
    def set_limit_distance(self, limit_distance):
        """Sets the limit distacne"""
        self.limit_distance = limit_distance
        