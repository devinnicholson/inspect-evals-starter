from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("inspect-evals-starter-with-policies")
except PackageNotFoundError:
    __version__ = "0.1.0"
