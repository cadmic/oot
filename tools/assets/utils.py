def str_removeprefix(string: str, prefix: str):
    if string.startswith(prefix):
        return string[len(prefix) :]
    else:
        return string


def str_removesuffix(string: str, suffix: str):
    if suffix and string.endswith(suffix):
        assert len(suffix) > 0
        return string[: -len(suffix)]
    else:
        return string
