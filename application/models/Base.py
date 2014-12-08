from application import db


# Base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    PROTECTED_ATTRIBUTES = ['id', 'date_created', 'date_modified']

    _id = db.Column(db.BigInteger, primary_key=True)
    _date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    _date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.get_id())

    def get_id(self):
        return self._id

    def get_date_created(self):
        return self._date_created

    def get_date_modified(self):
        return self._date_modified

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **updates):
        protected_attributes = []
        for attr in self.PROTECTED_ATTRIBUTES:
            if attr in updates:
                protected_attributes.append(attr)

        if protected_attributes:
            raise AttributeError(
                'Update to {} is not supported with changes to {}'.format(
                    self.__class__.__name__, ', '.join(protected_attributes)
                )
            )

        for attr, value in updates.iteritems():
            protected_attr = '_' + attr
            set_method = 'set_' + attr
            if hasattr(self, protected_attr) and hasattr(self, set_method):
                getattr(self, set_method)(value)

        self.save()

    # Define serialized form of the model
    @property
    def serialized(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.get_id(),
            'date_created': self.dump_datetime(self.get_date_created()),
            'date_modified': self.dump_datetime(self.get_date_modified())
        }

    @staticmethod
    def dump_datetime(value):
        """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
