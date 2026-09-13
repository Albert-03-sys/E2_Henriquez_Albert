class EscaneoException(Exception):
    """Excepción base para los errores del módulo de escaneo."""
    pass

class PuertoInvalidoError(EscaneoException):
    """Lanzada cuando se intenta escanear un puerto fuera del rango 1-65535."""
    pass