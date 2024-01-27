
class Move:
    def __init__(self, initial, final):
        # initial n final is square
        self.initial = initial
        self.final = final

    def __str__(self):
        s=''
        s+= f'{self.initial.row}{self.initial.col} -> {self.final.row}{self.final.col}'
        return s
    
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
