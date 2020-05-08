from . import base


class Ref(base.Base):
    """$ref expander."""

    key = '$ref'

    validator = base.PrimitiveDataValidator(
        input_type=str,
    )

    def expand(self):
        print(self.data)