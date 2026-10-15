# divyanshusood.github.io

Personal research site. Static, no build step, no dependencies to install.
Live at **https://divyanshusood.github.io**.

```
index.html        the site: overview, research, publications, teaching, graph, positions
kg.html           the interactive knowledge graph (embedded in the Graph tab, also standalone)
sood_kg.ttl       the same graph as RDF Turtle
assets/site.css   styles
assets/site.js    tab handling and the Voronoi hero
```

## Publishing

Pushing to `main` publishes the site. In the repository, **Settings → Pages** must have
Source set to *Deploy from a branch*, branch `main`, folder `/ (root)`. Changes go live
within a couple of minutes.

## Working on it locally

Open `index.html` over HTTP rather than double-clicking it, or the stylesheet and script
will not load:

```bash
python3 -m http.server 8765
```

Then visit http://localhost:8765.

## Editing

Content lives directly in `index.html`; there is no CMS or template layer. The knowledge
graph is generated: edit the entity lists at the top of `profile_kg/build_kg.py`, rerun it
and `render_kg.py`, then copy `sood_kg.html` here as `kg.html`.
