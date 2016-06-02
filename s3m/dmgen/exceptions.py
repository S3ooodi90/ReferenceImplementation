"""
application specific exceptions
"""


class S3MDatatypeError(Exception):
    pass


class PublishingError(Exception):
    pass


class AnnotationsError(Exception):
    pass


class ModellingError(Exception):
    pass


class GenerationError(Exception):
    pass


class CodesImportError(Exception):
    pass
