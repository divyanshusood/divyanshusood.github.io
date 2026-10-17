import json, io
# Paths resolve from this file, so the scripts run from any directory and write
# straight into the published site. No copy step, nothing to forget.
from pathlib import Path
HERE = Path(__file__).resolve().parent          # tools/kg
SITE = HERE.parent.parent                       # repo root, what GitHub Pages serves
DATA = HERE / "kg_data.json"

D=json.load(io.open(DATA,encoding='utf-8'))
HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Divyanshu Sood — Knowledge Graph</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{color-scheme:light;
 --surface:#fbfbfa; --glow:#ffffff; --panel:#ffffff; --ink:#0b0b0b; --sec:#54534f; --muted:#9a9a93;
 --line:#e4e4df; --edge:#c9c9c2;
 --role:#2a78d6; --project:#eb6834; --output:#1baf7a; --org:#9a9a94; --person:#141413;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;
 --surface:#131312; --glow:#20201e; --panel:#1e1e1c; --ink:#f7f7f4; --sec:#c3c2b7; --muted:#86867f;
 --line:#2e2e29; --edge:#3a3a34;
 --role:#3987e5; --project:#d95926; --output:#199e70; --org:#86867f; --person:#ffffff;}}
:root[data-theme="dark"]{color-scheme:dark;
 --surface:#131312; --glow:#20201e; --panel:#1e1e1c; --ink:#f7f7f4; --sec:#c3c2b7; --muted:#86867f;
 --line:#2e2e29; --edge:#3a3a34;
 --role:#3987e5; --project:#d95926; --output:#199e70; --org:#86867f; --person:#ffffff;}
*{box-sizing:border-box} html,body{margin:0;height:100%}
body{background:var(--surface);color:var(--ink);
 font:14px/1.55 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
 -webkit-font-smoothing:antialiased}
.shell{max-width:1560px;margin:0 auto;padding:22px 18px 28px}
h1{margin:0;font-size:23px;font-weight:650;letter-spacing:-.015em}
.sub{color:var(--sec);font-size:13.5px;margin-top:4px;max-width:70ch}
.bar{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin:16px 0 11px}
.chip{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:var(--panel);
 color:var(--ink);border-radius:999px;padding:5px 12px;font-size:12.5px;cursor:pointer;user-select:none;
 transition:opacity .16s,border-color .16s}
.chip:hover{border-color:var(--sec)}
.chip[aria-pressed="false"]{opacity:.35}
.mk{width:10px;height:10px;flex:none}
.mk.circle{border-radius:50%} .mk.square{border-radius:2.5px}
.spacer{flex:1}
button.plain{border:1px solid var(--line);background:var(--panel);color:var(--sec);border-radius:999px;
 padding:5px 12px;font-size:12.5px;cursor:pointer;transition:color .16s,border-color .16s}
button.plain:hover{color:var(--ink);border-color:var(--sec)}
.frame{position:relative;border:1px solid var(--line);border-radius:16px;overflow:hidden;
 background:radial-gradient(120% 90% at 50% 38%,var(--glow) 0%,var(--surface) 62%)}
svg{width:100%;height:86vh;min-height:660px;display:block;touch-action:none}
.link{fill:none;stroke:var(--edge);stroke-opacity:.5;transition:stroke .18s,stroke-opacity .18s}
.node{cursor:pointer}
.node path{stroke:var(--surface);stroke-width:2.2px}
.node text{font-size:10.5px;font-weight:500;fill:var(--sec);pointer-events:none;paint-order:stroke;
 stroke:var(--surface);stroke-width:3.4px;stroke-linejoin:round}
.node.org text{fill:var(--muted);font-weight:400}
.node.hub text{font-size:11.5px;font-weight:650;fill:var(--ink)}
.node.self text{font-size:14px;font-weight:700;fill:var(--ink)}
#tip{position:fixed;pointer-events:none;opacity:0;transform:translateY(4px);
 transition:opacity .14s,transform .14s;background:var(--panel);color:var(--ink);
 border:1px solid var(--line);border-radius:12px;padding:11px 13px;max-width:310px;font-size:12.5px;
 box-shadow:0 14px 40px rgba(0,0,0,.16);z-index:9}
#tip b{display:block;margin-bottom:4px;font-size:13.5px;font-weight:650}
#tip span{color:var(--sec);display:block}
#tip i{display:inline-block;margin-top:7px;font-style:normal;font-size:11px;color:var(--muted);
 text-transform:uppercase;letter-spacing:.07em}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--sec);font-weight:600;position:sticky;top:0;background:var(--surface)}
#tableView{display:none;max-height:86vh;overflow:auto}
.cap{color:var(--muted);font-size:12px;margin-top:11px;max-width:95ch}
</style></head><body>
<div class="shell">
  <h1>Divyanshu Sood</h1>
  <div class="sub">Roles, teaching, projects, outputs and the organisations that connect them. Node size follows how connected a thing is. Hover to isolate a neighbourhood; drag to rearrange.</div>
  <div class="bar" id="legend"></div>
  <div class="frame"><svg id="g"></svg></div>
  <div id="tableView"></div>
  <div class="cap" id="cap"></div>
</div>
<div id="tip" role="status"></div>
<script>
const DATA = __DATA__;
const CLS=[["role","Role","--role","circle"],["teaching","Teaching & supervision","--role","square"],
           ["project","Project","--project","circle"],["output","Output","--output","circle"],
           ["org","Organisation","--org","circle"]];
const HUE={person:"--person",role:"--role",teaching:"--role",project:"--project",output:"--output",org:"--org"};
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const colourOf=d=>css(HUE[d.cls]);

// degree drives size, so the hubs of the career read first
const deg={}; DATA.links.forEach(l=>{deg[l.source]=(deg[l.source]||0)+1; deg[l.target]=(deg[l.target]||0)+1;});
DATA.nodes.forEach(n=>n.deg=deg[n.id]||0);
const R=d=>d.cls==="person"?20:4.6+2.5*Math.sqrt(d.deg);
const SHAPE={teaching:d3.symbolSquare};
const sym=d=>d3.symbol().type(SHAPE[d.cls]||d3.symbolCircle)
                .size(Math.PI*R(d)*R(d)*(d.cls==="teaching"?0.86:1))();
const off=new Set();

const legend=document.getElementById("legend");
CLS.forEach(([k,label,v,shape])=>{
  const b=document.createElement("button");
  b.className="chip"; b.setAttribute("aria-pressed","true");
  b.innerHTML='<span class="mk '+shape+'" style="background:'+css(v)+'"></span>'+label;
  b.onclick=()=>{off.has(k)?off.delete(k):off.add(k);
    b.setAttribute("aria-pressed",off.has(k)?"false":"true"); redraw();};
  legend.appendChild(b);
});
const sp=document.createElement("div"); sp.className="spacer"; legend.appendChild(sp);
const tb=document.createElement("button"); tb.className="plain"; tb.textContent="Table"; legend.appendChild(tb);
const th=document.createElement("button"); th.className="plain"; th.textContent="Theme"; legend.appendChild(th);
document.getElementById("cap").textContent=
 "Four validated hues carry class identity and every node is directly labelled. Teaching and supervision share the Role hue but are drawn as squares, so the fifth class is distinguished by shape rather than an unvalidated fifth colour.";

const svg=d3.select("#g"), tip=document.getElementById("tip");
let link,node,sim;
const dims=()=>{const r=document.getElementById("g").getBoundingClientRect();return [r.width,r.height];};

function redraw(){
  const nodes=DATA.nodes.filter(n=>!off.has(n.cls)).map(d=>({...d}));
  const keep=new Set(nodes.map(n=>n.id));
  const links=DATA.links.filter(l=>keep.has(l.source.id||l.source)&&keep.has(l.target.id||l.target))
                        .map(l=>({...l,source:l.source.id||l.source,target:l.target.id||l.target}));
  svg.selectAll("*").remove();
  const [W,H]=dims();
  const defs=svg.append("defs");
  const f=defs.append("filter").attr("id","soft").attr("x","-55%").attr("y","-55%")
              .attr("width","210%").attr("height","210%");
  f.append("feDropShadow").attr("dx",0).attr("dy",1.4).attr("stdDeviation",2.2)
   .attr("flood-opacity",.26);

  link=svg.append("g").selectAll("path").data(links).join("path")
      .attr("class","link").attr("stroke-width",1.1);
  node=svg.append("g").selectAll("g").data(nodes).join("g")
      .attr("class",d=>"node "+d.cls+(d.cls==="person"?" self":(d.deg>=5?" hub":"")));
  node.append("path").attr("d",sym).attr("fill",colourOf).attr("filter","url(#soft)");
  node.append("text").attr("x",d=>R(d)+6).attr("dy","0.34em")
      .text(d=>d.label.length>26?d.label.slice(0,25)+"…":d.label);

  node.on("pointerenter",(ev,d)=>{
        tip.innerHTML="<b>"+d.label+"</b><span>"+(d.note||"")+"</span><i>"+
                      (d.cls==="person"?"subject":d.cls)+" · "+d.deg+" connections</i>";
        tip.style.opacity=1; tip.style.transform="translateY(0)"; move(ev);
        const nb=new Set([d.id]);
        links.forEach(l=>{if(l.source.id===d.id)nb.add(l.target.id);
                          if(l.target.id===d.id)nb.add(l.source.id);});
        node.style("opacity",x=>nb.has(x.id)?1:.14);
        link.attr("stroke",l=>(l.source.id===d.id||l.target.id===d.id)?colourOf(d):null)
            .attr("stroke-width",l=>(l.source.id===d.id||l.target.id===d.id)?1.9:1.1)
            .style("stroke-opacity",l=>(l.source.id===d.id||l.target.id===d.id)?.95:.07);})
      .on("pointermove",move)
      .on("pointerleave",()=>{tip.style.opacity=0;tip.style.transform="translateY(4px)";
        node.style("opacity",1);
        link.attr("stroke",null).attr("stroke-width",1.1).style("stroke-opacity",null);});
  function move(ev){tip.style.left=Math.min(ev.clientX+16,innerWidth-324)+"px";
                    tip.style.top=Math.min(ev.clientY+18,innerHeight-150)+"px";}

  const pad=16, lab=d=>Math.min(d.label.length,26)*5.5;
  sim=d3.forceSimulation(nodes)
    .force("link",d3.forceLink(links).id(d=>d.id)
           .distance(d=>d.target.cls==="org"?150:198).strength(.2))
    .force("charge",d3.forceManyBody().strength(-1150).distanceMax(900))
    .force("center",d3.forceCenter(W/2,H/2))
    .force("x",d3.forceX(W/2).strength(.03)).force("y",d3.forceY(H/2).strength(.055))
    .force("collide",d3.forceCollide().radius(d=>R(d)+17+lab(d)/2.1).iterations(3))
    .on("tick",()=>{
      nodes.forEach(d=>{d.x=Math.max(pad+R(d),Math.min(W-pad-R(d)-lab(d),d.x));
                        d.y=Math.max(pad+R(d),Math.min(H-pad-R(d),d.y));});
      link.attr("d",l=>{const dx=l.target.x-l.source.x, dy=l.target.y-l.source.y;
        const dr=Math.hypot(dx,dy)*2.6;   // gentle arc, so parallel edges separate
        return `M${l.source.x},${l.source.y}A${dr},${dr} 0 0,1 ${l.target.x},${l.target.y}`;});
      node.attr("transform",d=>`translate(${d.x},${d.y})`);});

  node.call(d3.drag()
    .on("start",(ev,d)=>{if(!ev.active)sim.alphaTarget(.3).restart();d.fx=d.x;d.fy=d.y;})
    .on("drag",(ev,d)=>{d.fx=ev.x;d.fy=ev.y;})
    .on("end",(ev,d)=>{if(!ev.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}));

  node.attr("opacity",0).transition().duration(520).delay((d,i)=>i*7).attr("opacity",1);
  link.attr("opacity",0).transition().duration(520).delay(160).attr("opacity",1);
}
function paint(){ if(node) node.select("path").attr("fill",colourOf);
  [...legend.querySelectorAll(".mk")].forEach((el,i)=>el.style.background=css(CLS[i][2])); }
th.onclick=()=>{const r=document.documentElement;
  const dark=getComputedStyle(r).getPropertyValue("--surface").trim()==="#131312";
  r.setAttribute("data-theme",dark?"light":"dark"); paint();};

const tv=document.getElementById("tableView");
tv.innerHTML="<table><thead><tr><th>Entity</th><th>Class</th><th>Detail</th><th>Connected to</th></tr></thead><tbody>"+
 DATA.nodes.slice().sort((a,b)=>b.deg-a.deg).map(n=>{
   const c=DATA.links.filter(l=>l.source===n.id||l.target===n.id).map(l=>l.source===n.id?l.target:l.source);
   return "<tr><td>"+n.label+"</td><td>"+n.cls+"</td><td>"+(n.note||"")+"</td><td>"+
          [...new Set(c)].join(", ")+"</td></tr>";}).join("")+"</tbody></table>";
tb.onclick=()=>{const t=tv.style.display==="block";
  tv.style.display=t?"none":"block";
  document.querySelector(".frame").style.display=t?"block":"none";
  tb.textContent=t?"Table":"Graph";};

redraw();

/* The graph can be laid out while hidden, for example inside a tab or an iframe that
   is not displayed yet. The SVG then measures zero and every node collapses into the
   corner. Watch for the element gaining real size and rebuild once it has. A short
   poll backs up the observer, because a zero-size box inside a display:none ancestor
   does not always report a resize. */
(function(){
  const g=document.getElementById("g");
  let built=dims()[0]>60;
  function spread(){const xs=[...g.querySelectorAll(".node")]
      .map(n=>+(n.getAttribute("transform")||"translate(0,0)").match(/translate\(([-\d.]+)/)[1]);
    return xs.length?Math.max(...xs)-Math.min(...xs):0;}
  function check(){
    const [W,H]=dims();
    if(W>60&&H>60&&(!built||spread()<W*0.25)){ built=true; redraw(); return true; }
    return false;
  }
  if(window.ResizeObserver) new ResizeObserver(check).observe(g);
  let n=0; const t=setInterval(()=>{ if(check()||++n>25) clearInterval(t); },400);
  let r; addEventListener("resize",()=>{clearTimeout(r);
    r=setTimeout(()=>{const [W,H]=dims(); if(W>60) redraw();},200);});
})();
</script></body></html>"""
io.open(SITE/'kg.html','w',encoding='utf-8').write(HTML.replace('__DATA__', json.dumps(D)))
print('kg.html rebuilt |', len(D['nodes']),'nodes')
