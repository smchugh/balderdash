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

    @classmethod
    def get(cls, record_id):
        return cls.query.filter_by(_id=record_id).first()

    @classmethod
    def get_list(cls, limit, offset):
        return cls.get_list_query(limit, offset).all()

    @classmethod
    def get_list_query(cls, limit, offset):
        return cls.query.order_by(cls._id).limit(limit).offset(offset)

    def get_id(self):
        return self._id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **updates):
        protected_attrs = []
        for attr in self.PROTECTED_ATTRIBUTES:
            if attr in updates:
                protected_attrs.append(attr)

        if protected_attrs:
            raise AttributeError(
                'update to {} is not supported with changes to {}'.format(
                    self.__class__.__name__, ', '.join(protected_attrs)
                )
            )

        for attr, value in updates.iteritems():
            pattr = '_' + attr
            if hasattr(self, pattr):
                setattr(self, pattr, value)

        self.save()

    # Define serialized form of the model
    @property
    def serialized(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self._id,
            'date_created': self.dump_datetime(self._date_created),
            'date_modified': self.dump_datetime(self._date_modified)
        }

    @staticmethod
    def dump_datetime(value):
        """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
