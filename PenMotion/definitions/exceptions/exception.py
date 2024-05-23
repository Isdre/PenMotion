from PenMotion.definitions.debugger import debug

class PenMotionException():
    def __init__(self, ctx, message):
        self.message = message + f' [{ctx}]'
        debug.logError(message)

    def __str__(self):
        return repr(self.message)