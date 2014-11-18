# Import flask dependencies
from flask import Blueprint

# Import input validators
from application.inputs.Words import ListInputs, CreateInputs, UpdateInputs

# Import models
from application.models.Word import Word

# Import view rendering
from application.controllers import get_inputs, render_view, get_mixed_dict_from_multidict

# Define the blueprint
words_module = Blueprint('words', __name__, url_prefix='/words')

# Set some common error constants
NOT_FOUND_ERROR = {'WordNotFound': ['Unable to find Word']}


# Set the route and accepted methods
@words_module.route('/', methods=['GET'])
def index():
    # Get the input validator
    inputs = ListInputs(get_inputs())

    # Verify the list inputs
    if inputs.validate():

        words = Word.get_list(inputs.limit.data, inputs.offset.data)

        return render_view('words/index', 200, words={word.get_id(): word.serialized for word in words})

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@words_module.route('/', methods=['POST'])
def create():
    # Get the input validator
    inputs = CreateInputs(get_inputs())

    # Verify the word creation inputs
    if inputs.validate_on_submit():

        word = Word(inputs.lexeme_form.data, inputs.lexical_class.data)
        try:
            word.save()
            return render_view('words/show', 201, word=word.serialized)
        except Exception as e:
            return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=inputs.serialized())

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@words_module.route('/<int:word_id>', methods=['GET'])
def show(word_id):
    # Get the word
    word = Word.get(word_id)

    if word:
        return render_view('words/show', 200, word=word.serialized)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': word_id})


# Set the route and accepted methods
@words_module.route('/<int:word_id>', methods=['PUT'])
def update(word_id):
    # Get the word
    word = Word.get(word_id)

    # Verify the word creation inputs
    if word:

        # Get the input validator
        inputs = UpdateInputs(get_inputs())
        combined_inputs = dict(inputs.serialized().items() + {'id': word_id}.items())

        if inputs.validate_on_submit():
            # If we're only marking the word as active or inactive, pass through to the update
            if inputs.is_active.data:
                try:
                    word.update(**get_mixed_dict_from_multidict(get_inputs(), inputs))
                    return render_view('words/show', 200, word=word.serialized)
                except Exception as e:
                    return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs)

            else:
                word.update(**{'is_active': False})

                lexeme_form = inputs.lexeme_form.data if inputs.lexeme_form.data else word.get_lexeme_form()
                lexical_class = inputs.lexical_class.data if inputs.lexical_class.data else word.get_lexical_class()

                word = Word(lexeme_form, lexical_class)

                try:
                    word.save()
                    return render_view(
                        'words/show', 200, word=word.serialized
                    )
                except Exception as e:
                    return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs)

        return render_view('422', 422, errors=inputs.errors, inputs=combined_inputs)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': word_id})


# Set the route and accepted methods
@words_module.route('/<int:word_id>', methods=['DELETE'])
def delete(word_id):
    # Get the word
    word = Word.get(word_id)

    # Verify the word creation inputs
    if word:
        try:
            word.update(**{'is_active': False})
            return render_view('words/show', 200, word=word.serialized)
        except Exception as e:
            return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs={'id': word_id})

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': word_id})
