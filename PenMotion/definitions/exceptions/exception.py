from PenMotion.definitions.debugger import debug

class PenMotionException():
    def __init__(self, ctx, scope, message):
        self.message = message + f' Scope:{scope} [{ctx}]'
        debug.logError(self.message)

    def __str__(self):
        return repr(self.message)