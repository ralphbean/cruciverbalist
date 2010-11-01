
class BaseMethod(object):
    def produce(self, puzzle):
        raise NotImplementedError, "%s must override produce" % (
            self.__class__.name )

