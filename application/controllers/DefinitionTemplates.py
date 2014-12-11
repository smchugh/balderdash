# Import flask dependencies
from flask import Blueprint

# Import input validators
from application.inputs.DefinitionTemplates import ListInputs, CreateInputs, UpdateInputs

# Import models
from application.models.DefinitionTemplate import DefinitionTemplate

# Import services
from application.services.WordsService import WordsService
from application.services.DefinitionTemplatesService import DefinitionTemplatesService

# Import view rendering
from application.controllers import get_inputs, render_view, get_mixed_dict_from_multidict

# Define the blueprint
definition_templates_module = Blueprint('definition_templates', __name__, url_prefix='/definition_templates')

# Set some common error constants
NOT_FOUND_ERROR = {'DefinitionTemplateNotFound': ['Unable to find DefinitionTemplate']}
WORD_NOT_FOUND_ERROR = {'WordNotFound': ['Unable to find the specified Word']}


# Set the route and accepted methods
@definition_templates_module.route('', methods=['GET'])
def index():
    """
    Request:
    {
        "offset": "offset",
        "limit": "limit",
        "word_id": "word_id"
    }

    Response [422] (invalid parameters):
    {
        "errors": {
            "name of parameter that failed validation": [
                "Reason for validation failure"
            ],
            "name of another parameter that failed validation": [
                "Reason for validation failure"
            ],
        },
        "inputs": {
            "offset": "value passed in. empty string if missing",
            "limit": "value passed in. empty string if missing",
            "word_id": "value passed in. empty string if missing"
        }
    }

    Response [200] (success):
    [
        {
            "id": "current value",
            "date_created": "current value",
            "date_modified": "current value",
            "word": "current value",
            "definition": "current value",
            "filler_lexical_classes": "current value",
            "is_active": "current value"
        },
        {
            "id": "current value",
            "date_created": "current value",
            "date_modified": "current value",
            "word": "current value",
            "definition": "current value",
            "filler_lexical_classes": "current value",
            "is_active": "current value"
        },
        ...
    ]
    """
    # Get the input validator
    inputs = ListInputs(get_inputs())

    # Verify the list inputs
    if inputs.validate():

        if inputs.word_id.data:
            definition_templates = DefinitionTemplatesService.get_instance().get_list_by_word(
                inputs.word_id.data, inputs.limit.data, inputs.offset.data
            )
        else:
            definition_templates = DefinitionTemplatesService.get_instance().get_list(
                inputs.limit.data, inputs.offset.data
            )

        return render_view(
            'definition_templates/index',
            200,
            definition_templates={
                definition_template.get_id(): definition_template.serialized
                for definition_template in definition_templates
            }
        )

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@definition_templates_module.route('', methods=['POST'])
def create():
    """
    Request:
    {
        "word_id": "word_id",
        "definition": "definition",
        "filler_lexical_classes": "filler_lexical_classes"
    }

    Response [422] (invalid parameters):
    {
        "errors": {
            "name of parameter that failed validation": [
                "Reason for validation failure"
            ],
            "name of another parameter that failed validation": [
                "Reason for validation failure"
            ],
        },
        "inputs": {
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing"
        }
    }

    Response [422] (word with word_id doesn't exist):
    {
        "errors": {
            "WordNotFound": [
                "Unable to find the specified Word"
            ]
        },
        "inputs": {
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure - invalid filler_lexical_classes length):
    {
        "errors": {
            "AttributeError": [
                "There are {} filler lexical classes but {} fillers. These values must be the same."
            ]
        },
        "inputs": {
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure - invalid filler_lexical_classes value):
    {
        "errors": {
            "AttributeError": [
                "Cannot set the filler lexical classes to a value other than one of: {}"
            ]
        },
        "inputs": {
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure):
    {
        "errors": {
            "IntegrityError": [
                "Reason saving to the db failed"
            ]
        },
        "inputs": {
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "word": "current value",
        "definition": "current value",
        "filler_lexical_classes": "current value",
        "is_active": "current value"
    }
    """
    # Get the input validator
    inputs = CreateInputs(get_inputs())

    # Verify the definition_template creation inputs
    if inputs.validate_on_submit():

        word = WordsService.get_instance().get(inputs.word_id.data)
        if word:
            try:
                definition_template = DefinitionTemplate(word, inputs.definition.data, inputs.filler_lexical_classes.data)
                definition_template.save()
                return render_view('definition_templates/show', 201, definition_template=definition_template.serialized)
            except Exception as e:
                return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=inputs.serialized())

        return render_view('422', 422, errors=WORD_NOT_FOUND_ERROR, inputs=inputs.serialized())

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@definition_templates_module.route('/<int:definition_template_id>', methods=['GET'])
def show(definition_template_id):
    """
    Request:
    {}

    Response [422] (definition_template with definition_template_id doesn't exist):
    {
        "errors": {
            "DefinitionTemplateNotFound": [
                "Unable to find DefinitionTemplate"
            ]
        },
        "inputs": {
            "id": "definition_template_id"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "word": "current value",
        "definition": "current value",
        "filler_lexical_classes": "current value",
        "is_active": "current value"
    }
    """
    # Get the definition_template
    definition_template = DefinitionTemplatesService.get_instance().get(definition_template_id)

    if definition_template:
        return render_view('definition_templates/show', 200, definition_template=definition_template.serialized)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': definition_template_id})


# Set the route and accepted methods
@definition_templates_module.route('/<int:definition_template_id>', methods=['PUT'])
def update(definition_template_id):
    """
    Request:
    {
        "word_id": "word_id",
        "definition": "definition",
        "filler_lexical_classes": "filler_lexical_classes",
        "is_active": "is_active"
    }

    Response [422] (definition_template with definition_template_id doesn't exist):
    {
        "errors": {
            "DefinitionTemplateNotFound": [
                "Unable to find DefinitionTemplate"
            ]
        },
        "inputs": {
            "id": "definition_template_id"
        }
    }

    Response [422] (invalid parameters):
    {
        "errors": {
            "name of parameter that failed validation": [
                "Reason for validation failure"
            ],
            "name of another parameter that failed validation": [
                "Reason for validation failure"
            ],
        },
        "inputs": {
            "id": "definition_template_id",
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [422] (word with word_id doesn't exist):
    {
        "errors": {
            "WordNotFound": [
                "Unable to find the specified Word"
            ]
        },
        "inputs": {
            "id": "definition_template_id",
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure - invalid filler_lexical_classes length):
    {
        "errors": {
            "AttributeError": [
                "There are {} filler lexical classes but {} fillers. These values must be the same."
            ]
        },
        "inputs": {
            "id": "definition_template_id",
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure - invalid filler_lexical_classes value):
    {
        "errors": {
            "AttributeError": [
                "Cannot set the filler lexical classes to a value other than one of: {}"
            ]
        },
        "inputs": {
            "id": "definition_template_id",
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure):
    {
        "errors": {
            "IntegrityError": [
                "Reason saving to the db failed"
            ]
        },
        "inputs": {
            "id": "definition_template_id",
            "word_id": "value passed in. empty string if missing",
            "definition": "value passed in. empty string if missing",
            "filler_lexical_classes": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "word": "current value",
        "definition": "current value",
        "filler_lexical_classes": "current value",
        "is_active": "current value"
    }
    """
    # Get the definition_template
    definition_template = DefinitionTemplatesService.get_instance().get(definition_template_id)

    # Verify the definition_template creation inputs
    if definition_template:

        # Get the input validator
        inputs = UpdateInputs(get_inputs())
        combined_inputs = dict(inputs.serialized().items() + {'id': definition_template_id}.items())

        if inputs.validate_on_submit():
            # If we're only marking the definition as active or inactive, pass through to the update
            if inputs.is_active.data and \
                    not any([inputs.word_id.data, inputs.definition.data, inputs.filler_lexical_classes.data]):
                try:
                    definition_template.update(**get_mixed_dict_from_multidict(get_inputs(), inputs))
                    return render_view(
                        'definition_templates/show', 200, definition_template=definition_template.serialized
                    )
                except Exception as e:
                    return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs)

            # Otherwise, if we're trying to change the definition, mark the old
            # definition as inactive and create a new one with the new parameters
            else:
                definition_template.update(**{'is_active': False})

                word = WordsService.get_instance().get(inputs.word_id.data) \
                    if inputs.word_id.data else definition_template.get_word()
                definition = inputs.definition.data if inputs.definition.data else definition_template.get_definition()
                filler_lexical_classes = inputs.filler_lexical_classes.data \
                    if inputs.filler_lexical_classes.data else definition_template.get_filler_lexical_classes()
                is_active = inputs.is_active.data if inputs.is_active.data else definition_template.get_is_active()

                if word:
                    try:
                        definition_template = DefinitionTemplate(word, definition, filler_lexical_classes)
                        definition_template.set_is_active(is_active)
                        definition_template.save()
                        return render_view(
                            'definition_templates/show', 200, definition_template=definition_template.serialized
                        )
                    except Exception as e:
                        return render_view(
                            '422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs
                        )

                return render_view('422', 422, errors=WORD_NOT_FOUND_ERROR, inputs=inputs.serialized())

        return render_view('422', 422, errors=inputs.errors, inputs=combined_inputs)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': definition_template_id})


# Set the route and accepted methods
@definition_templates_module.route('/<int:definition_template_id>', methods=['DELETE'])
def delete(definition_template_id):
    """
    Request:
    {}

    Response [422] (definition_template with definition_template_id doesn't exist):
    {
        "errors": {
            "DefinitionTemplateNotFound": [
                "Unable to find DefinitionTemplate"
            ]
        },
        "inputs": {
            "id": "definition_template_id"
        }
    }

    Response [422] (save failure - unable to set definition_template as inactive):
    {
        "errors": {
            "IntegrityError": [
                "Reason saving to the db failed"
            ]
        },
        "inputs": {
            "id": "definition_template_id"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "word": "current value",
        "definition": "current value",
        "filler_lexical_classes": "current value",
        "is_active": "current value"
    }
    """
    # Get the definition_template
    definition_template = DefinitionTemplatesService.get_instance().get(definition_template_id)

    # Verify the definition_template creation inputs
    if definition_template:
        try:
            definition_template.update(**{'is_active': False})
            return render_view('definition_templates/show', 200, definition_template=definition_template.serialized)
        except Exception as e:
            return render_view(
                '422', 422, errors={e.__class__.__name__: [e.message]}, inputs={'id': definition_template_id}
            )

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': definition_template_id})
