# Import Form for input validation
from flask.ext.wtf import Form


class Base(Form):
    def obfuscated(self):
        inputs = self.serialized()

        if inputs.get('password') is not None:
            inputs['password'] = None

        if inputs.get('confirm') is not None:
            inputs['confirm'] = None

        return inputs

    def serialized(self):
        inputs = {}
        for name in dir(self):
            if not name.startswith('__'):
                attribute = getattr(self, name)
                if hasattr(attribute, 'data'):
                    inputs[name] = attribute.data

        return inputs
