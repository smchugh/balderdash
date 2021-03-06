# Import flask dependencies
from flask import Blueprint

# Import input validators
from application.inputs.DefinitionFillers import ListInputs, CreateInputs, UpdateInputs

# Import models
from application.models.DefinitionFiller import DefinitionFiller

# Import services
from application.services.DefinitionFillersService import DefinitionFillersService
from application.services.DefinitionTemplatesService import DefinitionTemplatesService

# Import view rendering
from application.controllers import get_inputs, render_view, get_mixed_dict_from_multidict

# Define the blueprint
definition_fillers_module = Blueprint('definition_fillers', __name__, url_prefix='/definition_fillers')

# Set some common error constants
NOT_FOUND_ERROR = {'DefinitionFillerNotFound': ['Unable to find DefinitionFiller']}
DEFINITION_TEMPLATE_NOT_FOUND_ERROR = {
    'DefinitionTemplateNotFound': ['Unable to find the specified DefinitionTemplate']
}


# Set the route and accepted methods
@definition_fillers_module.route('', methods=['GET'])
def index():
    """
    Request:
    {
        "offset": "offset",
        "limit": "limit",
        "word_id": "word_id",
        "definition_template_id": "definition_template_id"
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
            "word_id": "value passed in. empty string if missing",
            "definition_template_id": "value passed in. empty string if missing"
        }
    }

    Response [200] (success):
    [
        {
            "id": "current value",
            "date_created": "current value",
            "date_modified": "current value",
            "definition_template": "current value",
            "filler": "current value",
            "is_dictionary": "current value",
            "is_active": "current value"
        },
        {
            "id": "current value",
            "date_created": "current value",
            "date_modified": "current value",
            "definition_template": "current value",
            "filler": "current value",
            "is_dictionary": "current value",
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
            definition_fillers = DefinitionFillersService.get_instance().get_list_by_word(
                inputs.word_id.data, inputs.limit.data, inputs.offset.data
            )
        elif inputs.definition_template_id.data:
            definition_fillers = DefinitionFillersService.get_instance().get_list_by_definition_template(
                inputs.definition_template_id.data, inputs.limit.data, inputs.offset.data
            )
        else:
            definition_fillers = DefinitionFillersService.get_instance().get_list(inputs.limit.data, inputs.offset.data)

        return render_view(
            'definition_fillers/index',
            200,
            definition_fillers={
                definition_filler.get_id(): definition_filler.serialized
                for definition_filler in definition_fillers
            }
        )

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@definition_fillers_module.route('', methods=['POST'])
def create():
    """
    Request:
    {
        "definition_template_id": "definition_template_id",
        "filler": "filler",
        "is_dictionary": "is_dictionary"
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
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing"
        }
    }

    Response [422] (definition_template with definition_template_id doesn't exist):
    {
        "errors": {
            "DefinitionTemplateNotFound": [
                "Unable to find the specified DefinitionTemplate"
            ]
        },
        "inputs": {
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing"
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
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure - invalid filler array length):
    {
        "errors": {
            "AttributeError": [
                "There are {} filler but {} filler lexical classes. These values must be the same"
            ]
        },
        "inputs": {
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "definition_template": "current value",
        "filler": "current value",
        "is_dictionary": "current value",
        "is_active": "current value"
    }
    """
    # Get the input validator
    inputs = CreateInputs(get_inputs())

    # Hack to deal with WTForms requirement that list inputs be validated against a list of choices
    filler = get_mixed_dict_from_multidict(get_inputs()).get('filler', [])
    inputs.filler.choices = [(fill, fill) for fill in filler]

    # Verify the definition_filler creation inputs
    if inputs.validate_on_submit():

        definition_template = DefinitionTemplatesService.get_instance().get(inputs.definition_template_id.data)
        if definition_template:
            try:
                definition_filler = DefinitionFiller(definition_template, inputs.filler.data, inputs.is_dictionary.data)
                definition_filler.save()
                return render_view('definition_fillers/show', 201, definition_filler=definition_filler.serialized)
            except Exception as e:
                return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=inputs.serialized())

        return render_view('422', 422, errors=DEFINITION_TEMPLATE_NOT_FOUND_ERROR, inputs=inputs.serialized())

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@definition_fillers_module.route('/<int:definition_filler_id>', methods=['GET'])
def show(definition_filler_id):
    """
    Request:
    {}

    Response [422] (definition_filler with definition_filler_id doesn't exist):
    {
        "errors": {
            "DefinitionFillerNotFound": [
                "Unable to find DefinitionFiller"
            ]
        },
        "inputs": {
            "id": "definition_filler_id"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "definition_template": "current value",
        "filler": "current value",
        "is_dictionary": "current value",
        "is_active": "current value"
    }
    """
    # Get the definition_filler
    definition_filler = DefinitionFillersService.get_instance().get(definition_filler_id)

    if definition_filler:
        return render_view('definition_fillers/show', 200, definition_filler=definition_filler.serialized)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': definition_filler_id})


# Set the route and accepted methods
@definition_fillers_module.route('/<int:definition_filler_id>', methods=['PUT'])
def update(definition_filler_id):
    """
    Request:
    {
        "definition_template_id": "definition_template_id",
        "filler": "filler",
        "is_dictionary": "is_dictionary",
        "is_active": "is_active"
    }

    Response [422] (definition_filler with definition_filler_id doesn't exist):
    {
        "errors": {
            "DefinitionFillerNotFound": [
                "Unable to find DefinitionFiller"
            ]
        },
        "inputs": {
            "id": "definition_filler_id"
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
            "id": "definition_filler_id",
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [422] (definition_template with definition_template_id doesn't exist):
    {
        "errors": {
            "DefinitionTemplateNotFound": [
                "Unable to find the specified DefinitionTemplate"
            ]
        },
        "inputs": {
            "id": "definition_filler_id",
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [422] (save failure - invalid filler array length):
    {
        "errors": {
            "AttributeError": [
                "There are {} filler but {} filler lexical classes. These values must be the same"
            ]
        },
        "inputs": {
            "id": "definition_filler_id",
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing",
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
            "id": "definition_filler_id",
            "definition_template_id": "value passed in. empty string if missing",
            "filler": "value passed in. empty string if missing",
            "is_dictionary": "value passed in. empty string if missing",
            "is_active": "value passed in. empty string if missing"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "definition_template": "current value",
        "filler": "current value",
        "is_dictionary": "current value",
        "is_active": "current value"
    }
    """
    # Get the definition_filler
    definition_filler = DefinitionFillersService.get_instance().get(definition_filler_id)

    # Verify the definition_filler creation inputs
    if definition_filler:

        # Get the input validator
        inputs = UpdateInputs(get_inputs())
        combined_inputs = dict(inputs.serialized().items() + {'id': definition_filler_id}.items())

        # Hack to deal with WTForms requirement that list inputs be validated against a list of choices
        filler = get_mixed_dict_from_multidict(get_inputs()).get('filler', [])
        inputs.filler.choices = [(fill, fill) for fill in filler]

        if inputs.validate_on_submit():
            # If we're only marking the filler as active or inactive, pass through to the update
            if inputs.is_active.data and \
                    not any([inputs.definition_template_id.data, inputs.filler.data, inputs.is_dictionary.data]):
                try:
                    definition_filler.update(**get_mixed_dict_from_multidict(get_inputs(), inputs))
                    return render_view(
                        'definition_fillers/show', 200, definition_filler=definition_filler.serialized
                    )
                except Exception as e:
                    return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs)

            # If we're trying to change the filler, mark the old filler
            # as inactive and create a new one with the new parameters
            else:
                definition_filler.update(**{'is_active': False})

                definition_template = DefinitionTemplatesService.get_instance().get(
                    inputs.definition_template_id.data
                ) if inputs.definition_template_id.data else definition_filler.get_definition_template()
                filler = inputs.filler.data if inputs.filler.data else definition_filler.get_filler()
                is_dictionary = inputs.is_dictionary.data \
                    if inputs.is_dictionary.data else definition_filler.get_is_dictionary()
                is_active = inputs.is_active.data if inputs.is_active.data else definition_filler.get_is_active()

                if definition_template:
                    try:
                        definition_filler = DefinitionFiller(definition_template, filler, is_dictionary)
                        definition_filler.set_is_active(is_active)
                        definition_filler.save()
                        return render_view(
                            'definition_fillers/show', 200, definition_filler=definition_filler.serialized
                        )
                    except Exception as e:
                        return render_view(
                            '422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs
                        )

                return render_view('422', 422, errors=DEFINITION_TEMPLATE_NOT_FOUND_ERROR, inputs=inputs.serialized())

        return render_view('422', 422, errors=inputs.errors, inputs=combined_inputs)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': definition_filler_id})


# Set the route and accepted methods
@definition_fillers_module.route('/<int:definition_filler_id>', methods=['DELETE'])
def delete(definition_filler_id):
    """
    Request:
    {}

    Response [422] (definition_filler with definition_filler_id doesn't exist):
    {
        "errors": {
            "DefinitionFillerNotFound": [
                "Unable to find DefinitionFiller"
            ]
        },
        "inputs": {
            "id": "definition_filler_id"
        }
    }

    Response [422] (save failure - unable to set definition_filler as inactive):
    {
        "errors": {
            "IntegrityError": [
                "Reason saving to the db failed"
            ]
        },
        "inputs": {
            "id": "definition_filler_id"
        }
    }

    Response [200] (success):
    {
        "id": "current value",
        "date_created": "current value",
        "date_modified": "current value",
        "definition_template": "current value",
        "filler": "current value",
        "is_dictionary": "current value",
        "is_active": "current value"
    }
    """
    # Get the definition_filler
    definition_filler = DefinitionFillersService.get_instance().get(definition_filler_id)

    # Verify the definition_filler creation inputs
    if definition_filler:
        try:
            definition_filler.update(**{'is_active': False})
            return render_view('definition_fillers/show', 200, definition_filler=definition_filler.serialized)
        except Exception as e:
            return render_view(
                '422', 422, errors={e.__class__.__name__: [e.message]}, inputs={'id': definition_filler_id}
            )

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': definition_filler_id})
