class BaseService(object):

    _instance = None

    def __init__(self, serviced_class):
        self._serviced_class = serviced_class

    def get_class(self):
        return self._serviced_class

    def get(self, record_id):
        return self.get_class().query.filter_by(_id=record_id).first()

    def get_list(self, limit=None, offset=None):
        return self.get_class().query.order_by(self.get_class()._id).limit(limit).offset(offset).all()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
