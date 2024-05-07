class Enviroment:
    def __int__(self):
        self.global_scope = {}
        self.scope_stack = []
        self.functions = {}