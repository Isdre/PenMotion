class Variable_():
    def __init__(self):
        self.type = None
        self.value = None

    def __repr__(self):
        return f"<Variable {self.type} : {self.value}>"

    def setValue(self, value):
        self.value = value
        self.type = type(value)

    def getValue(self):
        return self.value
