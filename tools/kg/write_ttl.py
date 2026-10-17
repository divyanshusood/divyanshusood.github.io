"""Regenerate sood_kg.ttl from kg_data.json so the RDF stays in step with the graph.

Previously the Turtle file was written once by hand, which meant it drifted the
moment build_kg.py changed. Run this after build_kg.py.
"""
import io
import json
import re
from datetime import date
# Paths resolve from this file, so the scripts run from any directory and write
# straight into the published site. No copy step, nothing to forget.
from pathlib import Path
HERE = Path(__file__).resolve().parent          # tools/kg
SITE = HERE.parent.parent                       # repo root, what GitHub Pages serves
DATA = HERE / "kg_data.json"


D = json.load(io.open(DATA, encoding="utf-8"))

CLASS = {
    "person": "foaf:Person",
    "org": "org:Organization",
    "role": "kg:Role",
    "project": "kg:Project",
    "output": "kg:Output",
    "teaching": "kg:TeachingActivity",
}

# graph relation label -> Turtle predicate, matching the vocabulary already published
PRED = {
    "holds": "kg:holdsRole",
    "at": "kg:heldAt",
    "works on": "kg:worksOn",
    "with": "kg:partner",
    "produced": "kg:produced",
    "led to": "kg:ledTo",
    "teaches or supervises": "kg:teachesOrSupervises",
    "coordinated as": "kg:coordinatedAs",
    "applied to": "kg:appliedTo",
    "evaluated in": "kg:evaluatedIn",
    "contributes to": "kg:contributesTo",
    "adopted by": "kg:adoptedBy",
    "presented to": "kg:presentedTo",
    "proposal with": "kg:proposalWith",
    "organised events for": "kg:organisedFor",
    "part of": "org:subOrganizationOf",
    "studied at": "kg:studiedAt",
}


def iri(label):
    """kg: local name, matching the convention in the published file."""
    s = re.sub(r"[^0-9A-Za-z]+", "_", label).strip("_")
    return "kg:" + s


def lit(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


unknown = {l["rel"] for l in D["links"]} - set(PRED)
assert not unknown, f"no predicate mapped for: {unknown}"

out = [
    "@prefix kg:   <https://divyanshusood.example/kg#> .",
    "@prefix foaf: <http://xmlns.com/foaf/0.1/> .",
    "@prefix org:  <http://www.w3.org/ns/org#> .",
    "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
    "",
    f"# Knowledge graph of Divyanshu Sood, generated {date.today().isoformat()}.",
    "# Classes: Role, TeachingActivity, Project, Output, Organization. Person is the subject.",
    f"# {len(D['nodes'])} entities, {len(D['links'])} relations.",
    "",
]

# group outgoing relations by subject so each entity is one block
edges = {}
for l in D["links"]:
    edges.setdefault(l["source"], []).append((PRED[l["rel"]], iri(l["target"])))

for n in D["nodes"]:
    subj = iri(n["id"])
    lines = [f"{subj} a {CLASS[n['cls']]} ;", f"    rdfs:label {lit(n['label'])}"]
    if n.get("note"):
        lines[-1] += " ;"
        lines.append(f"    rdfs:comment {lit(n['note'])}")
    for pred, obj in edges.get(n["id"], []):
        lines[-1] += " ;"
        lines.append(f"    {pred} {obj}")
    lines[-1] += " ."
    out.append("\n".join(lines))
    out.append("")

io.open(SITE/"sood_kg.ttl", "w", encoding="utf-8").write("\n".join(out))
print(f"sood_kg.ttl: {len(D['nodes'])} entities, {len(D['links'])} relations")
