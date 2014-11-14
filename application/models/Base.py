from application import db


# Base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **updates):
        for attr, value in updates.iteritems():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.save()

    @property
    def serialized(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'date_created': self.dump_datetime(self.date_created),
            'date_modified': self.dump_datetime(self.date_modified)
        }

    @staticmethod
    def dump_datetime(value):
        """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
