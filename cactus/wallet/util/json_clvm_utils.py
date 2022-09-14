from typing import Any

from cactus.types.blockchain_format.program import Program


def json_to_cactuslisp(json_data: Any) -> Any:
    list_for_cactuslisp = []
    if isinstance(json_data, list):
        for value in json_data:
            list_for_cactuslisp.append(json_to_cactuslisp(value))
    else:
        if isinstance(json_data, dict):
            for key, value in json_data:
                list_for_cactuslisp.append((key, json_to_cactuslisp(value)))
        else:
            list_for_cactuslisp = json_data
    return Program.to(list_for_cactuslisp)
