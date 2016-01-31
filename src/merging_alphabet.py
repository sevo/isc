import symbol_alphabet
import symbol

class MergingAlphabet(symbol_alphabet.SymbolAlphabet):
    
    def size(self):
        """Returns size of the alphabet"""
        pass

    def symbols(self):
        """Returns a list of stored symbols"""
        pass

    def distance(self, a, b):
        """Returns distacne between symbols"""
        pass
        
    def get_similar(self, normalized, symbol_shift):
        """Returns similar symbol from the alphabet"""
        pass