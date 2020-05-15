
class MsgPart:

    def __init__(self, text, **kwargs):
        self.text = text
        self.kwargs = kwargs

    def __str__(self):
        return self.text
