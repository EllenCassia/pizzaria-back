class ObjectSaveError(Exception):

    def __init__(self, message: str = "Failed to save the object.", *args):
        self.message = message
        super().__init__(self.message, *args)
