import re
from ..types import Field, InputObjectType, String
from ..types.mutation import Mutation
from ..utils.thenables import maybe_thenable


class ClientIDMutation(Mutation):


    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, output=None, input_fields=None,
        arguments=None, name=None, **options):
        input_class = getattr(cls, 'Input', None)
        base_name = re.sub('Payload$', '', name or cls.__name__)
        assert not output, "Can't specify any output"
        assert not arguments, "Can't specify any arguments"
        bases = InputObjectType,
        if input_class:
            bases += input_class,
        if not input_fields:
            input_fields = {}
        cls.Input = type(f'{base_name}Input', bases, dict(input_fields,
            client_mutation_id=String(name='clientMutationId')))
        arguments = dict(input=cls.Input(required=True))
        mutate_and_get_payload = getattr(cls, 'mutate_and_get_payload', None)
        if (cls.mutate and cls.mutate.__func__ == ClientIDMutation.mutate.
            __func__):
            assert mutate_and_get_payload, f'{name or cls.__name__}.mutate_and_get_payload method is required in a ClientIDMutation.'
        if not name:
            name = f'{base_name}Payload'
        super(ClientIDMutation, cls).__init_subclass_with_meta__(output=
            None, arguments=arguments, name=name, **options)
        cls._meta.fields['client_mutation_id'] = Field(String, name=
            'clientMutationId')
