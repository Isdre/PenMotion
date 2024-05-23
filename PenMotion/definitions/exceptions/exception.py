class PenMotionException(Exception):
    def __init__(self, ctx, message):
        self.message = message + f' [{ctx}]'

    def __str__(self):
        return repr(self.message)