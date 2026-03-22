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
__all__ = ["ARCH", "OWL", "RDF", "RDFS", "SH", "XSD", "bind_namespaces"]


def bind_namespaces(graph: Graph) -> Graph:
    """Bind all standard prefixes to an rdflib Graph."""
    graph.bind("arch", ARCH)
    graph.bind("owl", OWL)
    graph.bind("rdfs", RDFS)
    graph.bind("sh", SH)
    graph.bind("xsd", XSD)
    return graph
