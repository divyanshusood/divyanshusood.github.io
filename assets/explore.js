/* Explore: four interactive pieces.
   Each one makes a published finding playable. The numbers are representative
   profiles chosen to behave like the real thing, not output from NEDT; every
   panel says so on the page. Amber is reserved for "at or over capacity",
   matching the rest of the site. */
(function(){
  const TEAL='#0e4f63', AMBER='#c87f12', RULE='#e2e8ec', SEC='#56656f', MUTED='#8b98a1';
  const PF=0.95;                      /* power factor, kW -> kVA */
  const H=[...Array(24).keys()];

  /* ---- per-dwelling mean profiles, kW. Diversity is already inside these. ---- */
  const P={
    baseW:[.35,.30,.28,.27,.28,.32,.45,.65,.70,.60,.55,.55,.58,.55,.55,.62,.85,1.20,1.45,1.40,1.20,.95,.70,.48],
    baseS:[.30,.26,.24,.23,.24,.28,.40,.58,.62,.52,.48,.48,.50,.48,.48,.52,.65,.85,1.05,1.05,.95,.80,.60,.42],
    hpW:  [.55,.55,.55,.60,.70,.90,1.30,1.50,1.30,1.00,.85,.80,.78,.78,.80,.95,1.20,1.45,1.50,1.35,1.10,.90,.70,.60],
    hpS:  [.18,.18,.18,.18,.20,.25,.35,.40,.32,.25,.22,.20,.20,.20,.20,.22,.28,.35,.38,.34,.28,.24,.20,.19],
    evUn: [.25,.20,.15,.10,.10,.10,.15,.20,.15,.10,.10,.10,.12,.12,.15,.25,.55,1.35,1.80,1.70,1.35,.95,.60,.35],
    evSm: [.95,1.10,1.15,1.10,.95,.70,.35,.20,.12,.10,.10,.10,.10,.10,.12,.15,.20,.30,.35,.35,.40,.55,.75,.90],
    pvW:  [0,0,0,0,0,0,0,0,.05,.25,.55,.80,.90,.85,.60,.30,.08,0,0,0,0,0,0,0],
    pvS:  [0,0,0,0,.05,.25,.60,1.10,1.70,2.30,2.80,3.05,3.10,2.95,2.60,2.10,1.50,.90,.45,.15,.02,0,0,0]
  };
  /* Fewer customers means less diversity, so each home contributes a larger
     share of its own peak. This is why small rural stations bite first. */
  const div=n=>1+1.2/Math.sqrt(n);

  /* Net load per hour for a district, in kW. */
  function profile(o){
    const base=o.summer?P.baseS:P.baseW, hp=o.summer?P.hpS:P.hpW,
          pv=o.summer?P.pvS:P.pvW, ev=o.smart?P.evSm:P.evUn, d=div(o.homes);
    return H.map(h=>{
      const heat=o.hp*hp[h]*(1-0.35*o.retro);   /* a B2 retrofit cuts heat demand */
      return o.homes*d*(base[h]+heat+o.ev*ev[h]-o.pv*pv[h]);
    });
  }
  const util=(kw,kva)=>100*(kw/PF)/kva;

  /* ---------- tiny SVG chart helpers ---------- */
  const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
  function axes(W,Ht,m,yMax,yMin,ticks,xlabs){
    const y=v=>m.t+(yMax-v)/(yMax-yMin)*(Ht-m.t-m.b);
    let s='';
    ticks.forEach(t=>{ s+=`<line x1="${m.l}" y1="${y(t).toFixed(1)}" x2="${W-m.r}" y2="${y(t).toFixed(1)}" stroke="${RULE}" stroke-width="1"/>`
      +`<text x="${m.l-7}" y="${(y(t)+3.6).toFixed(1)}" text-anchor="end" font-size="10" fill="${MUTED}" font-family="Space Grotesk,sans-serif">${t}</text>`; });
    const bw=(W-m.l-m.r)/xlabs.length;
    xlabs.forEach((l,i)=>{ if(l==='') return;
      s+=`<text x="${(m.l+bw*(i+.5)).toFixed(1)}" y="${Ht-m.b+14}" text-anchor="middle" font-size="10" fill="${MUTED}" font-family="Space Grotesk,sans-serif">${esc(l)}</text>`; });
    return {g:s,y,bw};
  }
  const path=(pts)=>pts.map((p,i)=>(i?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' ');

  /* ================= 1. Transformer challenge ================= */
  const G1={rating:400,homes:85};
  function drawG1(){
    const o={hp:+v('g1hp')/100, ev:+v('g1ev')/100, pv:+v('g1pv')/100, retro:+v('g1re')/100,
             summer:document.getElementById('g1season').checked,
             smart:document.getElementById('g1smart').checked, homes:G1.homes};
    const load=profile(o), kva=load.map(k=>k/PF);
    const peak=Math.max(...kva), pk=kva.indexOf(peak), u=100*peak/G1.rating;
    const over=kva.filter(k=>k>G1.rating).length;

    /* what drove the peak hour */
    const base=o.summer?P.baseS:P.baseW, hpP=o.summer?P.hpS:P.hpW,
          pvP=o.summer?P.pvS:P.pvW, evP=o.smart?P.evSm:P.evUn, d=div(o.homes);
    const drivers=[['heat pumps',o.hp*hpP[pk]*(1-0.35*o.retro)],
                   ['EV charging',o.ev*evP[pk]]].sort((a,b)=>b[1]-a[1]);

    const W=680,Ht=250,m={l:38,r:12,t:14,b:26};
    const yMax=Math.max(G1.rating*1.35, peak*1.12), ts=[0,150,300,450,600].filter(t=>t<=yMax);
    const A=axes(W,Ht,m,yMax,0,ts,H.map(h=>h%3===0?h+':00':''));
    let bars='';
    kva.forEach((k,i)=>{ const x=m.l+A.bw*i+A.bw*0.14, w=A.bw*0.72,
      yy=A.y(Math.max(k,0)), hh=Math.max(A.y(0)-yy,0.6);
      bars+=`<rect x="${x.toFixed(1)}" y="${yy.toFixed(1)}" width="${w.toFixed(1)}" height="${hh.toFixed(1)}" rx="2" fill="${k>G1.rating?AMBER:TEAL}" opacity="${k>G1.rating?.92:.80}"><title>${i}:00 — ${Math.round(k)} kVA</title></rect>`; });
    const cy=A.y(G1.rating);
    const cap=`<line x1="${m.l}" y1="${cy.toFixed(1)}" x2="${W-m.r}" y2="${cy.toFixed(1)}" stroke="${AMBER}" stroke-width="1.6" stroke-dasharray="5 4"/>`
      +`<text x="${W-m.r}" y="${(cy-6).toFixed(1)}" text-anchor="end" font-size="10.5" fill="${AMBER}" font-family="Space Grotesk,sans-serif">${G1.rating} kVA rating</text>`;
    document.getElementById('g1chart').innerHTML=
      `<svg viewBox="0 0 ${W} ${Ht}" role="img" aria-label="Half-hourly district load against the ${G1.rating} kVA transformer rating. Peak ${Math.round(peak)} kVA at ${pk}:00, ${u.toFixed(0)} per cent of rating.">${A.g}${bars}${cap}</svg>`;

    const band=u<=85?['ok','Headroom','Normal ageing']
              :u<=100?['warn','Tight','Normal ageing, little margin']
              :u<=115?['bad','Over capacity','Elevated thermal ageing']
                     :['bad','Well over capacity','Accelerated thermal ageing'];
    document.getElementById('g1out').innerHTML=
      `<div class="xp-stat"><b>${u.toFixed(0)}%</b><span>of rating at peak</span></div>`+
      `<div class="xp-stat"><b>${Math.round(peak)}</b><span>kVA peak, at ${pk}:00</span></div>`+
      `<div class="xp-stat"><b>${over}</b><span>hours over capacity</span></div>`;
    document.getElementById('g1msg').innerHTML=
      `<span class="xp-pill ${band[0]}">${band[1]}</span> ${band[2]}. `+
      (drivers[0][1]>0.02
        ? `Largest electrification driver at the peak hour: <b>${drivers[0][0]}</b>, adding `+
          `${Math.round(drivers[0][1]*o.homes*div(o.homes)/PF)} kVA.`
        : `The peak is still set by ordinary household demand.`)+
      (o.pv>0&&!o.summer?` Solar adds nothing at ${pk}:00, because the winter peak falls after dark.`:'');
  }

  /* ================= 2. Urban against rural ================= */
  function drawG2(){
    const smart=document.getElementById('g2smart').checked;
    const feeders=[
      {n:'Dublin suburb',  rating:400, homes:85, c:TEAL},
      {n:'Rural town, Co. Leitrim', rating:50, homes:12, c:AMBER}
    ];
    const xs=[...Array(21).keys()].map(i=>i*5);          /* 0..100 % uptake */
    const series=feeders.map(f=>({...f, y:xs.map(p=>{
      const l=profile({hp:p/100,ev:p/100,pv:0,retro:0,summer:false,smart,homes:f.homes});
      return util(Math.max(...l), f.rating);
    })}));
    const W=680,Ht=250,m={l:38,r:14,t:14,b:26};
    const yMax=Math.max(180,...series.flatMap(s=>s.y))*1.04;
    const A=axes(W,Ht,m,yMax,0,[0,50,100,150,200].filter(t=>t<=yMax),xs.map(x=>x%20===0?x+'%':''));
    const X=i=>m.l+A.bw*(i+.5);
    let g='';
    const cy=A.y(100);
    g+=`<line x1="${m.l}" y1="${cy.toFixed(1)}" x2="${W-m.r}" y2="${cy.toFixed(1)}" stroke="${SEC}" stroke-width="1.4" stroke-dasharray="5 4"/>`
      +`<text x="${m.l+4}" y="${(cy-6).toFixed(1)}" font-size="10.5" fill="${SEC}" font-family="Space Grotesk,sans-serif">100% of rating</text>`;
    const breaches=[];
    series.forEach(s=>{
      g+=`<path d="${path(s.y.map((v,i)=>[X(i),A.y(v)]))}" fill="none" stroke="${s.c}" stroke-width="2.2" stroke-linejoin="round"/>`;
      let b=null;
      for(let i=1;i<s.y.length;i++) if(s.y[i-1]<100&&s.y[i]>=100){
        const t=(100-s.y[i-1])/(s.y[i]-s.y[i-1]); b=xs[i-1]+t*(xs[i]-xs[i-1]); break; }
      if(b!==null){ const px=m.l+A.bw*(b/5+.5);
        g+=`<circle cx="${px.toFixed(1)}" cy="${cy.toFixed(1)}" r="4.5" fill="${s.c}" stroke="#fff" stroke-width="2"/>`;
        breaches.push({n:s.n,b:Math.round(b),c:s.c}); }
    });
    document.getElementById('g2chart').innerHTML=
      `<svg viewBox="0 0 ${W} ${Ht}" role="img" aria-label="Transformer utilisation against national electrification uptake for two contrasting feeders. ${breaches.map(x=>x.n+' breaches at '+x.b+' per cent').join('; ')}.">${A.g}${g}</svg>`;
    document.getElementById('g2legend').innerHTML=series.map(s=>
      `<span class="xp-key"><i style="background:${s.c}"></i>${esc(s.n)} &middot; ${s.homes} homes on ${s.rating} kVA</span>`).join('');
    document.getElementById('g2out').innerHTML=series.map(s=>{
      const b=breaches.find(x=>x.n===s.n);
      return `<div class="xp-stat"><b style="color:${s.c}">${b?b.b+'%':'never'}</b>`+
        `<span>${b?'uptake before ':''}${esc(s.n.split(',')[0])}${b?' breaches':' stays within rating'}</span></div>`;
    }).join('');
    const why=' because 50 kVA pole-mounted units serve far fewer homes, so each one contributes more of its own peak.';
    document.getElementById('g2msg').innerHTML=
      breaches.length===2
        ? `One national target, two very different outcomes. The rural feeder runs out of capacity <b>${Math.abs(breaches[0].b-breaches[1].b)} percentage points</b> of uptake earlier than the suburb,`+why
        : breaches.length===1
          ? `Smart charging keeps the suburb within rating across the whole range, but the rural feeder still breaches at <b>${breaches[0].b}%</b> uptake,`+why
          : `Neither feeder breaches across this range.`;
  }

  /* ================= 3. Read the load curve ================= */
  let truth=null;
  const rnd=()=>Math.round(Math.random()*16)*5/100;        /* 0 .. 0.80 in 5% steps */
  function newRound(){ truth={hp:rnd(),ev:rnd(),pv:rnd()};
    document.getElementById('g3reveal').hidden=true; drawG3(); }
  function curve(o){ return profile({...o,retro:0,summer:false,smart:false,homes:85}); }
  function drawG3(){
    if(!truth) return;
    const guess={hp:+v('g3hp')/100, ev:+v('g3ev')/100, pv:+v('g3pv')/100};
    const t=curve(truth), g=curve(guess);
    const W=680,Ht=250,m={l:38,r:12,t:14,b:26};
    const yMax=Math.max(...t,...g)*1.12, ts=[0,100,200,300,400,500].filter(x=>x<=yMax);
    const A=axes(W,Ht,m,yMax,0,ts,H.map(h=>h%3===0?h+':00':''));
    const X=i=>m.l+A.bw*(i+.5);
    const sv=`<svg viewBox="0 0 ${W} ${Ht}" role="img" aria-label="A mystery district load curve with your guess overlaid.">${A.g}`+
      `<path d="${path(t.map((y,i)=>[X(i),A.y(y)]))}" fill="none" stroke="${TEAL}" stroke-width="2.6"/>`+
      `<path d="${path(g.map((y,i)=>[X(i),A.y(y)]))}" fill="none" stroke="${AMBER}" stroke-width="2" stroke-dasharray="6 4"/></svg>`;
    document.getElementById('g3chart').innerHTML=sv;
    const err=(Math.abs(guess.hp-truth.hp)+Math.abs(guess.ev-truth.ev)+Math.abs(guess.pv-truth.pv))/3;
    const score=Math.max(0,Math.round(100-err*300));
    document.getElementById('g3out').innerHTML=
      `<div class="xp-stat"><b>${score}</b><span>match score out of 100</span></div>`;
  }
  function reveal(){
    const r=document.getElementById('g3reveal');
    r.hidden=false;
    r.innerHTML=`The mystery curve was <b>${Math.round(truth.hp*100)}%</b> heat pumps, `+
      `<b>${Math.round(truth.ev*100)}%</b> electric vehicles and <b>${Math.round(truth.pv*100)}%</b> rooftop solar. `+
      `Each leaves its own mark: heat pumps lift the whole winter day and add a morning shoulder, `+
      `uncontrolled EV charging makes a sharp spike just after six, and solar scoops out the middle of the day.`;
  }

  /* ================= 4. Power Ireland for a day ================= */
  const DEM=[3.4,3.2,3.1,3.0,3.05,3.3,3.8,4.3,4.5,4.4,4.3,4.3,4.35,4.3,4.3,4.45,4.9,5.4,5.5,5.3,5.0,4.6,4.1,3.7];
  const WCF=[.62,.65,.68,.70,.68,.64,.58,.50,.42,.36,.32,.30,.33,.38,.45,.52,.58,.62,.66,.70,.72,.70,.66,.64];
  const SCF=[0,0,0,0,0,0,0,0,.02,.09,.17,.22,.24,.21,.14,.06,.01,0,0,0,0,0,0,0];
  function drawG4(){
    const wind=+v('g4w'), sol=+v('g4s'), gasC=+v('g4g'), batP=+v('g4b'), ic=+v('g4i');
    const batE=batP*4;                                  /* four-hour battery */
    let soc=batE*0.5, res=[],gas=[],imp=[],bat=[],cur=[],uns=[];
    H.forEach(h=>{
      const r=Math.min(wind*WCF[h]+sol*SCF[h], 99), d=DEM[h];
      let used=Math.min(r,d), net=d-used, curt=r-used, b=0;
      if(curt>0){ const room=Math.min(batP, batE-soc, curt); soc+=room*0.92; curt-=room; b=-room; }
      if(net>0){ const dis=Math.min(batP, soc, net); soc-=dis; net-=dis; b=dis; }
      const i=Math.min(ic,net); net-=i;
      const g=Math.min(gasC,net); net-=g;
      res.push(used); gas.push(g); imp.push(i); bat.push(b); cur.push(curt); uns.push(net);
    });
    const tot=DEM.reduce((a,b)=>a+b,0);
    const resSh=100*(res.reduce((a,b)=>a+b,0)+Math.max(0,bat.reduce((a,b)=>a+b,0)))/tot;
    const unsT=uns.reduce((a,b)=>a+b,0), gasT=gas.reduce((a,b)=>a+b,0), curT=cur.reduce((a,b)=>a+b,0);
    const co2=gasT*1000*0.37;                           /* ~0.37 tCO2 per MWh, CCGT */

    const W=680,Ht=250,m={l:38,r:12,t:14,b:26};
    const yMax=Math.max(6.2,...DEM)*1.1;
    const A=axes(W,Ht,m,yMax,0,[0,2,4,6],H.map(h=>h%3===0?h+':00':''));
    const layers=[['Renewables',res,TEAL,.85],['Battery',bat.map(x=>Math.max(x,0)),'#3f8ea6',.9],
                  ['Import',imp,'#8fb3bf',.95],['Gas',gas,SEC,.75],['Unserved',uns,AMBER,.95]];
    let bars='';
    H.forEach(h=>{
      let acc=0;
      layers.forEach(([,arr,c,op])=>{ const vv=arr[h]; if(vv<=0.001) return;
        const y0=A.y(acc), y1=A.y(acc+vv);
        bars+=`<rect x="${(m.l+A.bw*h+A.bw*.14).toFixed(1)}" y="${y1.toFixed(1)}" width="${(A.bw*.72).toFixed(1)}" height="${Math.max(y0-y1,.5).toFixed(1)}" fill="${c}" opacity="${op}"/>`;
        acc+=vv; });
    });
    const dl=path(DEM.map((d,i)=>[m.l+A.bw*(i+.5),A.y(d)]));
    document.getElementById('g4chart').innerHTML=
      `<svg viewBox="0 0 ${W} ${Ht}" role="img" aria-label="Hourly dispatch against demand. Renewable share ${resSh.toFixed(0)} per cent, unserved energy ${unsT.toFixed(1)} gigawatt hours.">${A.g}${bars}`+
      `<path d="${dl}" fill="none" stroke="#101b24" stroke-width="1.8" stroke-dasharray="4 3"/></svg>`;
    document.getElementById('g4legend').innerHTML=
      layers.map(([n,,c])=>`<span class="xp-key"><i style="background:${c}"></i>${n}</span>`).join('')+
      `<span class="xp-key"><i style="background:#101b24"></i>Demand</span>`;
    document.getElementById('g4out').innerHTML=
      `<div class="xp-stat"><b${resSh>=80?' style="color:'+TEAL+'"':''}>${resSh.toFixed(0)}%</b><span>renewable share</span></div>`+
      `<div class="xp-stat"><b${unsT>0.05?' style="color:'+AMBER+'"':''}>${unsT.toFixed(1)}</b><span>GWh unserved</span></div>`+
      `<div class="xp-stat"><b>${Math.round(co2).toLocaleString()}</b><span>tonnes CO<sub>2</sub></span></div>`+
      `<div class="xp-stat"><b>${curT.toFixed(1)}</b><span>GWh curtailed</span></div>`;
    document.getElementById('g4msg').innerHTML= unsT>0.05
      ? `<span class="xp-pill bad">Lights out</span> ${unsT.toFixed(1)} GWh of demand went unmet. Firm capacity has to cover the hours when the wind drops.`
      : resSh>=80
        ? `<span class="xp-pill ok">Target met</span> You cleared 80% renewable electricity with the lights on. Note how much you had to curtail to get there.`
        : `<span class="xp-pill warn">Keeping the lights on</span> Supply meets demand, but renewables are at ${resSh.toFixed(0)}%, short of the 80% target for 2030.`;
  }

  /* ---------- wiring ---------- */
  function v(id){ return document.getElementById(id).value; }
  function bind(ids,fn){ ids.forEach(id=>{ const el=document.getElementById(id); if(!el) return;
    const lab=document.querySelector(`[data-for="${id}"]`);
    const sync=()=>{ if(lab) lab.textContent=el.type==='range'?el.value+(el.dataset.unit||'%'):''; fn(); };
    el.addEventListener('input',sync); sync(); }); }

  if(!document.getElementById('g1chart')) return;
  bind(['g1hp','g1ev','g1pv','g1re','g1season','g1smart'],drawG1);
  bind(['g2smart'],drawG2);
  bind(['g3hp','g3ev','g3pv'],drawG3);
  bind(['g4w','g4s','g4g','g4b','g4i'],drawG4);
  document.getElementById('g3new').addEventListener('click',newRound);
  document.getElementById('g3show').addEventListener('click',reveal);
  newRound();
})();
