import uuid

class BaseMethod(object):
    def __init__(self, id=None):
        self.id = id
        if not self.id:
            self.id = datetime.datetime.today().strftime('%F-%T')
        print "WORKING WITH UUID: %s" % self.id

    def produce(self, puzzle):
        raise NotImplementedError, "%s must override produce" % (
            self.__class__.name )

