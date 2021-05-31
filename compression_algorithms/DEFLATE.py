import zlib, base64


def deflate(data: str):
    data = data.encode("UTF-8")
    data = base64.b64encode(data)
    compressed = zlib.compress(data)
    return compressed


def inflate(data: bytes):
    decompressed = zlib.decompress(data)
    decompressed = base64.b64decode(decompressed)
    result = decompressed.decode("UTF-8")
    return result
