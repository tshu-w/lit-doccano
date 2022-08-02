r"""
To test a lightning component:

1. Init the component.
2. call .run()
"""
from lit_doccano.component import LitDoccano


def test_doccano_component():
    messenger = LitDoccano()
    messenger.run()
    assert messenger.value == 1
