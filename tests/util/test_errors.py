from __future__ import annotations

from cactus.util.errors import Err
from cactus.util.ints import int16


def test_error_codes_int16() -> None:
    # Make sure all Err codes fit into int16 because its part of the ProtocolMessageTypes.error message structure
    for err in Err:
        assert int16(err.value) == err.value
