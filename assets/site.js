/* Tabs: plain buttons driving section visibility, with the hash kept in sync
   so a section can be linked to directly. */
(function(){
  const btns=[...document.querySelectorAll('nav button, .tabbar button')];
  const secs=[...document.querySelectorAll('main section')];
  function show(id,push){
    btns.forEach(b=>b.setAttribute('aria-current', String(b.dataset.go===id)));
    secs.forEach(s=>s.classList.toggle('on', s.id===id));
    /* The graph needs the full page width, so the sidebar gives way to a
       horizontal strip for that one section. */
    document.body.classList.toggle('graph-wide', id==='graph');
    if(push && location.hash.slice(1)!==id) history.replaceState(null,'','#'+id);
    const h=document.getElementById(id); if(h) h.focus({preventScroll:true});
    /* Section ids double as deep links, so the browser would otherwise scroll past
       the header to the section element. Keep the reader where they expect to be. */
    if(push) document.querySelector('.shell').scrollIntoView({behavior:'smooth',block:'start'});
  }
  btns.forEach(b=>b.addEventListener('click',()=>show(b.dataset.go,true)));
  const start=location.hash.slice(1);
  show(secs.some(s=>s.id===start)?start:'overview',false);
  if(start) requestAnimationFrame(()=>window.scrollTo(0,0));
  addEventListener('hashchange',()=>{const id=location.hash.slice(1);
    if(secs.some(s=>s.id===id)) show(id,false);});
})();

/* Hero: a capacity-weighted Voronoi field. Each seed is a notional transformer
   station; cell area stands for its catchment. A few cells are flagged at capacity.
   This is the subject's own method used as the page's one piece of ornament. */
(function(){
  const svg=document.getElementById('voronoi'); if(!svg||!window.d3) return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  let pts=[], w=0, h=0, raf=null;
  const N=150;
  function seed(){
    const box=svg.getBoundingClientRect(); w=Math.max(box.width,320); h=Math.max(box.height,260);
    svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
    pts=d3.range(N).map(()=>({x:Math.random()*w,y:Math.random()*h,
      vx:(Math.random()-.5)*.08,vy:(Math.random()-.5)*.08,
      hot:Math.random()<.055}));
  }
  function frame(){
    const del=d3.Delaunay.from(pts,p=>p.x,p=>p.y);
    const vor=del.voronoi([0,0,w,h]);
    let cells='',dots='';
    for(let i=0;i<pts.length;i++){
      const poly=vor.renderCell(i); if(!poly) continue;
      cells+=`<path d="${poly}" fill="${pts[i].hot?'rgba(200,127,18,.14)':'rgba(14,79,99,.028)'}" `+
             `stroke="${pts[i].hot?'rgba(200,127,18,.5)':'rgba(14,79,99,.17)'}" stroke-width=".9"/>`;
      dots+=`<circle cx="${pts[i].x.toFixed(1)}" cy="${pts[i].y.toFixed(1)}" r="${pts[i].hot?2:1.3}" `+
            `fill="${pts[i].hot?'#c87f12':'rgba(14,79,99,.45)'}"/>`;
    }
    svg.innerHTML=cells+dots;
    if(!reduce){
      for(const p of pts){p.x+=p.vx;p.y+=p.vy;
        if(p.x<0||p.x>w)p.vx*=-1; if(p.y<0||p.y>h)p.vy*=-1;}
      raf=requestAnimationFrame(frame);
    }
  }
  function start(){ if(raf)cancelAnimationFrame(raf); seed(); frame(); }
  start();
  let t; addEventListener('resize',()=>{clearTimeout(t);t=setTimeout(start,180);});
})();
