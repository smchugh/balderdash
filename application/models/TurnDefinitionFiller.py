from application import db
from application.models.Base import Base


class TurnDefinitionFiller(Base):

    __tablename__ = 'turn_definition_fillers'

    PROTECTED_ATTRIBUTES = [
        'turn_id', 'turn', 'definition_template_id', 'definition_template',
        'fillers', 'is_dictionary', 'supplier_id', 'selector_id'
    ]

    _turn_id = db.Column(db.BigInteger, db.ForeignKey('turns._id'), nullable=False)
    _definition_template_id = db.Column(db.BigInteger, db.ForeignKey('definition_templates._id'), nullable=False)
    _filler = db.Column(db.PickleType())
    # True if this is the filler used to generate the dictionary definition
    _is_dictionary = db.Column(db.Boolean, nullable=False, default=False)
    # This is the ID of the opponent who supplied this filler, NULL for game-generated filler
    _supplier_id = db.Column(db.BigInteger, db.ForeignKey('players._id'))
    # This is the ID of the player who selected the definition generated from this filler,
    # NULL for all the other fillers assigned to this turn
    _selector_id = db.Column(db.BigInteger, db.ForeignKey('players._id'))

    def __init__(self, turn, definition_template, filler, is_dictionary, supplier=None):
        self._set_turn(turn)
        self._set_definition_template(definition_template)
        self._set_filler(filler)
        self._set_is_dictionary(is_dictionary)
        self._set_supplier(supplier)

    def get_turn(self):
        return self.turn

    def _set_turn(self, turn):
        self.turn = turn
        return self

    def get_definition_template(self):
        return self.definition_template

    def _set_definition_template(self, definition_template):
        self.definition_template = definition_template
        return self

    def get_filler(self):
        return self._filler

    def _set_filler(self, filler):
        self._filler = filler
        return self

    def get_is_dictionary(self):
        return self._is_dictionary

    def _set_is_dictionary(self, is_dictionary):
        self._is_dictionary = is_dictionary
        return self

    def get_supplier(self):
        return self.supplier

    def get_supplier_id(self):
        return self._supplier_id

    def _set_supplier(self, supplier):
        self.supplier = supplier
        return self

    def get_selector(self):
        return self.selector

    def get_selector_id(self):
        return self._selector_id

    def set_selector(self, selector):
        self.selector = selector
        return self

    def get_definition(self):
        definition_template = self.get_definition_template()
        if not definition_template:
            raise AttributeError(
                'Turn definition filler {} does not have a definition_template assigned'.format(self.get_id())
            )

        definition_text = definition_template.get_definition()
        if not definition_text:
            raise AttributeError(
                'Defintion template {} does not have definition text'.format(definition_template.get_id())
            )

        filler = self.get_filler()
        if not filler:
            raise AttributeError(
                'Turn definition filler {} does not have filler defined'.format(self.get_id())
            )

        return definition_text.format(**filler)

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(TurnDefinitionFiller, self).serialized
        turn_definition_filler_properties = {
            'definition': self.get_definition(),
            'is_dictionary': self.get_is_dictionary(),
            'supplier_id': self.get_supplier_id(),
            'selector_id': self.get_selector_id()
        }
        return dict(base_properties.items() + turn_definition_filler_properties.items())
