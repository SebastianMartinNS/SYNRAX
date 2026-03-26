"""synrax/namespaces.py — Central RDF namespace definitions for ArchGraph.

exports: ARCH, SYNRAX, bind_namespaces(graph)
used_by: synrax/extract/*.py | synrax/schema/*.py | synrax/query/*.py
rules:   All RDF namespaces MUST be defined here. Never create ad-hoc Namespace() elsewhere.
agent:   claude-opus-4 | anthropic | 2026-03-22 | Initial namespace definitions from ArchGraph spec.
"""

from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDF, RDFS, SH, XSD

# ArchGraph ontology namespace
ARCH = Namespace("http://archgraph.example.org/")

# Convenience re-exports
__all__ = [
    "ARCH",
    "OWL",
    "RDF",
    "RDFS",
    "SH",
    "XSD",
    "bind_namespaces",
    "make_module_uri",
    "uri_to_path",
]


def bind_namespaces(graph: Graph) -> Graph:
    """Bind all standard prefixes to an rdflib Graph."""
    graph.bind("arch", ARCH)
    graph.bind("owl", OWL)
    graph.bind("rdfs", RDFS)
    graph.bind("sh", SH)
    graph.bind("xsd", XSD)
    return graph


_SEPARATOR = "::"


def make_module_uri(module_path: str) -> str:
    """Create a URI-safe identifier from a module file path.

    Uses '::' as separator to avoid ambiguity with underscores in filenames.
    E.g. 'forms/order_form.py' -> 'forms::order_form'
         'forms/order/form.py' -> 'forms::order::form'
    """
    return module_path.replace("\\", "/").replace(".py", "").replace("/", _SEPARATOR)


def uri_to_path(uri_fragment: str) -> str:
    """Convert URI fragment back to a file path.

    Reverse of make_module_uri.
    E.g. 'forms::order_form' -> 'forms/order_form.py'
         'forms::order::form' -> 'forms/order/form.py'
    """
    return uri_fragment.replace(_SEPARATOR, "/") + ".py"
