import json, io
# Paths resolve from this file, so the scripts run from any directory and write
# straight into the published site. No copy step, nothing to forget.
from pathlib import Path
HERE = Path(__file__).resolve().parent          # tools/kg
SITE = HERE.parent.parent                       # repo root, what GitHub Pages serves
DATA = HERE / "kg_data.json"


P="Divyanshu Sood"
N=[]; L=[]
def n(id,cls,label,note=""): N.append({"id":id,"cls":cls,"label":label,"note":note})
def e(a,b,rel): L.append({"source":a,"target":b,"rel":rel})

n(P,"person",P,"Mechanical engineer; spatial energy systems modelling, machine learning, teaching")

# ---------------- organisations (neutral) ----------------
orgs={
 "UCD":"University College Dublin","UCD Energy Institute":"UCD Energy Institute",
 "NexSys":"NexSys national energy systems programme","SEAI":"Sustainable Energy Authority of Ireland",
 "ESB":"ESB Networks","CODEMA":"Dublin's local authority energy agency","ARUP":"ARUP",
 "PMVT":"Peter McVerry Trust","TU Dublin":"TU Dublin","Defence Forces":"Irish Defence Forces",
 "Bus Eireann":"Bus Eireann","Wind Energy Ireland":"Wind Energy Ireland","EPRI":"EPRI",
 "IEA EBC":"IEA Energy in Buildings and Communities","IPCC":"Intergovernmental Panel on Climate Change",
 "Engineers Ireland":"Engineers Ireland","NSAI":"NSAI","DTU":"Technical University of Denmark",
 "UCL":"University College London","Surrey":"University of Surrey","UL":"University of Limerick",
 "IIT Delhi":"IIT Delhi","TERI":"TERI, New Delhi","Chitkara":"Chitkara University",
 "ASHRAE":"ASHRAE","IBPSA":"IBPSA","EU TalentOn":"EU TalentOn, European Commission",
 "EC3":"European Conference on Computing in Construction",
}
for k,v in orgs.items(): n(k,"org",k,v)

# ---------------- roles ----------------
roles=[
 ("Senior Energy Systems Researcher","Apr 2025 to present","UCD Energy Institute"),
 ("Module Coordinator","Energy Systems in Buildings II, Sept 2025 to present","UCD"),
 ("Data Theme Lead","Data and IP Sub-Committee, from 2026","NexSys"),
 ("Ireland Representative","IEA EBC Annex 95, six activities","IEA EBC"),
 ("IPCC Reviewer","AR7 Special Report on Climate Change and Cities","IPCC"),
 ("Member, Engineers Ireland","MIEI; Chartered Engineer route begun","Engineers Ireland"),
 ("NSAI Young Professional","Standards participation","NSAI"),
 ("NSAI Committee Member","Three technical committees: energy performance of buildings, retrofit, energy management","NSAI"),
 ("IEC Young Professional","2026; one of two Irish nominees, nominated by NSAI","NSAI"),
 ("Research Assistant","Oct 2024 to Mar 2025","UCD"),
 ("Doctoral Researcher","Sept 2020 to Sept 2024, SEAI ALIVE Scholarship","UCD"),
 ("Project Associate","Jan to Aug 2020","TERI"),
 ("Junior Research Fellow","Jul to Dec 2019","IIT Delhi"),
]
for r,note,org in roles:
    n(r,"role",r,note); e(P,r,"holds"); e(r,org,"at")

# ---------------- projects ----------------
projects=[
 ("NEDT","National Energy Digital Twin: dwellings to LV transformer districts; scenarios, thermal ageing, driver attribution",["UCD Energy Institute","NexSys","ESB"]),
 ("Ask NEDT","Retrieval-augmented interface; retrieve-or-compute routing and evaluation harness",["UCD Energy Institute"]),
 ("Overload benchmark","Reliability of ML for transformer overload screening under distribution shift",["UCD Energy Institute"]),
 ("DER disaggregation","Heat pump, EV and solar adoption from aggregate feeder signals",["UCD Energy Institute"]),
 ("Knowledge graph framework","Transformer-level planning with traceable provenance",["UCD Energy Institute"]),
 ("Last Mile of Net Zero","Urban versus rural electrification glide-paths",["UCD Energy Institute"]),
 ("ReserveLens","Grid services from data centre UPS batteries; safety as a hard constraint",["EU TalentOn"]),
 ("Climate and electricity systems","Seven-person multi-disciplinary UCD team",["UCD"]),
 ("Intelligent data harvesting","Computer vision and generative methods for building stock classification",["UCD"]),
 ("V2H charging optimisation","Cost-minimising charging under tariffs; peak load cut by half",["UCD"]),
 ("Retrofit carbon assessment","Operational and embodied carbon across a social housing portfolio",["ARUP","PMVT"]),
 ("PhD: occupancy and IEQ","Bayesian neural networks and hidden Markov models; sensors in occupied homes",["UCD"]),
 ("Room-level occupancy simulator","Research visit",["DTU"]),
 ("Probabilistic occupancy model","Research visit",["UCL"]),
 ("PCM envelope optimisation","Phase change materials, DSC over 1000 cycles, genetic algorithm",["IIT Delhi"]),
 ("Vacuum insulation panels","Real-gas conductivity model; service life revised down",["IIT Delhi"]),
]
for pr,note,os_ in projects:
    n(pr,"project",pr,note); e(P,pr,"works on")
    for o in os_: e(pr,o,"with")

# ---------------- outputs and recognition ----------------
outputs=[
 ("19 journal papers","Q1 journals, 659 citations, h-index 10, i10-index 10",[]),
 ("13 conference papers","Peer-reviewed, including three at EC3 2026",["EC3"]),
 ("Building & Environment 2024","Physics-informed ML validated at 1.9% CVRMSE, R2 0.99",["Intelligent data harvesting"]),
 ("NeurIPS AI4Grid 2026","Under review; accuracy tuning degrades the safety metric",["Overload benchmark"]),
 ("CISP-BMEI 2026","Signal processing track",["DER disaggregation"]),
 ("EC3 2026 pedagogy paper","Dual-assessment masters module design, evaluated and published",["Module Coordinator"]),
 ("Policy paper","Indoor air quality and ventilation in new homes, publicpolicy.ie",["PhD: occupancy and IEQ"]),
 ("NSAI Standards Innovation Award","2024",["NSAI"]),
 ("CIBSE Young Modeller Award","2023",[]),
 ("EU TalentOn 2026","European Commission, selected participant",["ReserveLens"]),
 ("EYEF 2026","European Youth Energy Forum, one of 100 participants worldwide, Nice",[]),
 ("EC3 2026 knowledge graph paper","A utility-aware knowledge graph to support multi-scale residential energy modelling",["Knowledge graph framework","EC3"]),
 ("EC3 2026 low-code paper","Low-code toolchain development to accelerate data-driven energy modelling",["Knowledge graph framework","EC3"]),
 ("Building & Environment 2026","A review of research on multi-stakeholder approaches to sustainable built environments",["Ireland Representative"]),
 ("Overload label dataset","Station-level overload and thermal-risk labels, published on Zenodo; sole author",["Overload benchmark"]),
 ("CIBSE Building Simulation Award","2024, runner up",[]),
 ("Thesis in 3","2024, winner, IBPSA Ireland symposium",["IBPSA"]),
]
for o,note,src in outputs:
    n(o,"output",o,note); e(P,o,"produced")
    for s in src: e(s,o,"led to")

# ---------------- teaching and supervision ----------------
# drawn in the Role hue but as squares: a fifth legend entry without a fifth hue,
# because only three categorical hues pass all-pairs validation in both modes.
teaching=[
 ("Energy Systems in Buildings II","Core postgraduate module; thermodynamics, heat transfer, fluid dynamics, psychrometrics, load calculation, HVAC design",["UCD"]),
 ("Measurement and Instrumentation","Teaching assistant, 2020 to 2023",["UCD"]),
 ("Energy Conservation in Buildings","Teaching assistant, 2019",["IIT Delhi"]),
 ("Dual-assessment design","Half lectures, half project work; building simulation in IES VE, moved from Simergy",[]),
 ("Master's dissertations","Co-supervision of taught ME and MSc dissertation projects",["UCD"]),
 ("Final-year projects","Co-supervision of undergraduate final-year projects",["UCD"]),
 ("Research interns","Two interns on life cycle assessment of retrofit strategies; recruiting one for the digital twin",["ARUP","PMVT"]),
]
for t,note,os_ in teaching:
    n(t,"teaching",t,note); e(P,t,"teaches or supervises")
    for o in os_: e(t,o,"at")
e("Energy Systems in Buildings II","Module Coordinator","coordinated as")
e("Dual-assessment design","Energy Systems in Buildings II","applied to")
e("Dual-assessment design","EC3 2026 pedagogy paper","evaluated in")
e("Research interns","NEDT","contributes to")

# adoption edges
for a in ["CODEMA","TU Dublin","Defence Forces","ARUP","PMVT"]: e("PhD: occupancy and IEQ",a,"adopted by")
for s in ["SEAI","ESB","Bus Eireann","Wind Energy Ireland","EPRI"]: e("NEDT",s,"presented to")
for c in ["Surrey","UL"]: e(P,c,"proposal with")
for a in ["ASHRAE","IBPSA"]: e(P,a,"organised events for")
e("UCD Energy Institute","UCD","part of")
e(P,"Chitkara","studied at"); e(P,"TERI","studied at"); e(P,"UCD","studied at")

ids={x["id"] for x in N}
missing={l["source"] for l in L}|{l["target"] for l in L}
assert missing<=ids, "dangling: %s" % (missing-ids)
json.dump({"nodes":N,"links":L}, io.open(DATA,'w',encoding='utf-8'), indent=1)
from collections import Counter
print("nodes", len(N), dict(Counter(x["cls"] for x in N)), "| edges", len(L))
