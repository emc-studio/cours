{
const D=JSON.parse(document.getElementById('data').textContent);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const toast=m=>{const t=document.getElementById('toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1800)};
const copy=async(txt,msg)=>{try{await navigator.clipboard.writeText(txt);toast(msg||'Copié')}catch(e){toast('Copie refusée par le navigateur')}};
const cp=document.getElementById('copyPatch');
if(cp&&D.patch)cp.addEventListener('click',()=>copy(JSON.stringify(D.patch,null,1),'Patch copié : File › New From Clipboard dans Max'));
document.querySelectorAll('.code .copy').forEach(b=>b.addEventListener('click',()=>copy(b.closest('.code').querySelector('pre').textContent)));

/* ---------- patch ---------- */
const svg=document.getElementById('patch');
if(svg&&D.patch){
 const P=D.patch.patcher,B={};P.boxes.forEach(o=>B[o.box.id]=o.box);
 const port=(i,n,w)=>n<=1?4:4+i*(w-8)/(n-1);
 const fiche=b=>{const c=b.maxclass;const t=c==='message'?'message':c==='newobj'?String(b.text||'').split(' ')[0]:c;return D.tok[t]};
 let h='';
 P.lines.forEach(l=>{const [s,so]=l.patchline.source,[d,di]=l.patchline.destination;const a=B[s],b=B[d];if(!a||!b)return;
  const [ax,ay,aw,ah]=a.patching_rect,[bx,by,bw]=b.patching_rect;
  const x1=ax+port(so,a.numoutlets,aw),y1=ay+ah,x2=bx+port(di,b.numinlets,bw),y2=by,k=Math.max(12,Math.abs(y2-y1)*.4);
  const mp=l.patchline.midpoints;let p;
  if(mp&&mp.length){p=`M${x1} ${y1}`;for(let i=0;i<mp.length;i+=2)p+=` L${mp[i]} ${mp[i+1]}`;p+=` L${x2} ${y2}`}
  else p=`M${x1} ${y1} C${x1} ${y1+k} ${x2} ${y2-k} ${x2} ${y2}`;
  const sig=(a.outlettype||[])[so]==='signal';
  h+=`<g class="cord" data-a="${s}" data-b="${d}"><path d="${p}" fill="none" stroke="var(--${sig?'acc':'mut'})" stroke-width="${sig?1.6:1}"${sig?'':' stroke-dasharray="3 3"'}/></g>`});
 const T=(x,y,s,fill,w)=>`<text x="${x}" y="${y}" font-size="11.5" font-family="Manrope,sans-serif" fill="${fill}"${w?` font-weight="${w}"`:''}>${s}</text>`;
 P.boxes.forEach(o=>{const b=o.box,[x,y,w,hh]=b.patching_rect,c=b.maxclass;let g='';
  if(c==='comment'){g=T(x+3,y+14,esc(b.text),b.bgcolor?'var(--acct)':'var(--mut)',b.bgcolor?600:400)}
  else if(c==='toggle'){g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--bg)" stroke="var(--ink)"/><path d="M${x+6} ${y+6}L${x+w-6} ${y+hh-6}M${x+w-6} ${y+6}L${x+6} ${y+hh-6}" stroke="var(--mut)"/>`}
  else if(c==='ezdac~'){g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--bg)" stroke="var(--ink)"/><path d="M${x+12} ${y+18}h6l8-7v24l-8-7h-6z" fill="var(--ink)"/><path d="M${x+30} ${y+16}q5 7 0 14M${x+34} ${y+12}q9 11 0 22" stroke="var(--ink)" fill="none"/>`}
  else if(c==='ezadc~'){g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--bg)" stroke="var(--ink)"/><rect x="${x+w/2-5}" y="${y+9}" width="10" height="17" rx="5" fill="var(--ink)"/><path d="M${x+w/2-9} ${y+20}q0 10 9 10q9 0 9-10M${x+w/2} ${y+30}v6" stroke="var(--ink)" fill="none" stroke-width="1.5"/>`}
  else if(c==='live.gain~'){const nm=((b.saved_attribute_attributes||{}).valueof||{}).parameter_shortname||'live.gain~';g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--bg)" stroke="var(--ink)"/>`+T(x+w/2-nm.length*3,y+13,esc(nm),'var(--ink)')+`<rect x="${x+6}" y="${y+20}" width="${w-12}" height="7" fill="none" stroke="var(--mut)"/><rect x="${x+6}" y="${y+20}" width="${(w-12)*.55}" height="7" fill="var(--acc)" opacity=".7"/><path d="M${x+6+(w-12)*.82} ${y+29}l-4 7h8z" fill="var(--ink)"/>`}
  else if(c==='attrui'){g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--msg)" stroke="var(--line)"/>`+T(x+6,y+15,esc(b.attr||'attrui'),'var(--ink)')+`<line x1="${x+w/2}" y1="${y+3}" x2="${x+w/2}" y2="${y+hh-3}" stroke="var(--line)"/>`}
  else if(c==='umenu'){const it=(b.items||[]).join(' ').split(' , ');g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--msg)" stroke="var(--ink)" rx="3"/>`+T(x+6,y+15,esc(it[it.length-1]||'umenu'),'var(--ink)')+`<path d="M${x+w-14} ${y+9}l4 5 4-5z" fill="var(--ink)"/>`}
  else if(c==='filtergraph~'){const yy=y+hh*.45;g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--bg)" stroke="var(--ink)"/><line x1="${x}" y1="${yy}" x2="${x+w}" y2="${yy}" stroke="var(--line)"/><path d="M${x+8} ${y+hh-4} C${x+w*.2} ${yy+4} ${x+w*.28} ${yy} ${x+w*.4} ${yy} L${x+w-4} ${yy}" fill="none" stroke="var(--acc)" stroke-width="1.6"/>`+T(x+6,y+14,'filtergraph~','var(--mut)')}
  else if(c==='flonum'||c==='number'){g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--bg)" stroke="var(--ink)"/><path d="M${x+4} ${y+6}l6 5-6 5z" fill="var(--ink)"/>`+T(x+14,y+15,c==='flonum'?'0.':'0','var(--ink)')}
  else{const msg=c==='message';const parts=esc(b.text||c).split(' ');const head=parts.shift();
   const rest=parts.map(p=>p.startsWith('@')?`<tspan fill="var(--acct)">${p}</tspan>`:p).join(' ');
   g=`<rect class="body" x="${x}" y="${y}" width="${w}" height="${hh}" fill="var(--${msg?'msg':'bg'})" stroke="${msg?'var(--line)':'var(--ink)'}" rx="${msg?4:0}"/>`+
    (msg?T(x+5,y+15,esc(b.text),'var(--ink)'):`<text x="${x+5}" y="${y+15}" font-size="11.5" font-family="Manrope,sans-serif" fill="var(--ink)"><tspan font-weight="700">${head}</tspan> <tspan fill="var(--mut)">${rest}</tspan></text>`);
   for(let i=0;i<b.numinlets;i++)g+=`<rect x="${x+port(i,b.numinlets,w)-3}" y="${y}" width="6" height="2" fill="var(--ink)"/>`;
   for(let i=0;i<b.numoutlets;i++)g+=`<rect x="${x+port(i,b.numoutlets,w)-3}" y="${y+hh-2}" width="6" height="2" fill="var(--ink)"/>`}
  const f=fiche(b),label=c==='newobj'||c==='message'?b.text:c;
  h+=`<g class="bx" data-id="${b.id}"${f?` data-f="${f}"`:''}><title>${esc(label)}${f?' (cliquer pour la fiche)':''}</title>${g}</g>`});
 Object.entries(D.pins).forEach(([n,[x,y]])=>{h+=`<g class="pin" data-s="${n}" tabindex="0" role="button" aria-label="Étape ${n}"><circle cx="${x}" cy="${y}" r="10"/><text x="${x}" y="${y+4}" text-anchor="middle" font-size="11.5" font-weight="600" font-family="Manrope,sans-serif">${n}</text></g>`});
 svg.innerHTML=h;
 const setStep=n=>{const ids=D.zones[n]||[];svg.classList.toggle('focus',!!n);
  svg.querySelectorAll('.bx').forEach(g=>g.classList.toggle('on',ids.includes(g.dataset.id)));
  svg.querySelectorAll('.cord').forEach(g=>g.classList.toggle('on',ids.includes(g.dataset.a)||ids.includes(g.dataset.b)));
  svg.querySelectorAll('.pin').forEach(g=>g.classList.toggle('on',g.dataset.s==n));
  document.querySelectorAll('.step').forEach(s=>s.classList.toggle('on',s.dataset.s==n))};
 let cur=0;
 svg.addEventListener('click',e=>{const p=e.target.closest('.pin');if(p){cur=cur==p.dataset.s?0:+p.dataset.s;setStep(cur);return}
  const b=e.target.closest('.bx');if(b&&b.dataset.f){const el=document.getElementById(b.dataset.f);if(el){location.hash=b.dataset.f;el.scrollIntoView({behavior:'smooth'})}}});
 svg.addEventListener('keydown',e=>{const p=e.target.closest('.pin');if(p&&(e.key==='Enter'||e.key===' ')){e.preventDefault();cur=+p.dataset.s;setStep(cur)}});
 document.querySelectorAll('.step').forEach(s=>{const go=()=>{cur=+s.dataset.s;setStep(cur)};s.addEventListener('mouseenter',go);s.addEventListener('focus',go);s.addEventListener('click',go)});
 const st=document.getElementById('steps');if(st)st.addEventListener('mouseleave',()=>{cur=0;setStep(0)});
}

/* ---------- spat demo ---------- */
const room=document.getElementById('room');
if(room){
 const cx=200,cy=200,R=110,spk=[[-45,1],[45,2],[-135,3],[135,4]];
 const pos=(a,r)=>[cx+r*Math.sin(a*Math.PI/180),cy-r*Math.cos(a*Math.PI/180)];
 let az=0,di=1,drag=false;
 const draw=()=>{let s=`<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="var(--line)"/><line x1="${cx}" y1="22" x2="${cx}" y2="378" stroke="var(--line)"/><line x1="22" y1="${cy}" x2="378" y2="${cy}" stroke="var(--line)"/>`+
  `<text x="${cx}" y="14" text-anchor="middle" font-size="12" fill="var(--mut)" font-family="JetBrains Mono,monospace">0° devant</text><text x="392" y="${cy-8}" text-anchor="end" font-size="12" fill="var(--mut)" font-family="JetBrains Mono,monospace">90°</text><text x="8" y="${cy-8}" font-size="12" fill="var(--mut)" font-family="JetBrains Mono,monospace">−90°</text><text x="${cx}" y="396" text-anchor="middle" font-size="12" fill="var(--mut)" font-family="JetBrains Mono,monospace">180°</text>`;
  spk.forEach(([a,n])=>{const [x,y]=pos(a,R);s+=`<rect x="${x-12}" y="${y-12}" width="24" height="24" fill="var(--ink)"/><text x="${x}" y="${y+4}" text-anchor="middle" font-size="12" font-weight="600" fill="var(--bg)" font-family="JetBrains Mono,monospace">${n}</text>`});
  s+=`<circle cx="${cx}" cy="${cy}" r="5" fill="var(--mut)"/>`;
  const [sx,sy]=pos(az,di/2*R);s+=`<line x1="${cx}" y1="${cy}" x2="${sx}" y2="${sy}" stroke="var(--acc)" stroke-dasharray="3 3"/><circle cx="${sx}" cy="${sy}" r="13" fill="var(--acc)" style="cursor:grab"/><text x="${sx}" y="${sy+4}" text-anchor="middle" font-size="12" font-weight="600" fill="#fff" pointer-events="none" font-family="JetBrains Mono,monospace">1</text>`;
  room.innerHTML=s;
  const a=((az%360)+360)%360,ring=[[45,2],[135,4],[225,3],[315,1]],g={1:0,2:0,3:0,4:0};
  for(let i=0;i<4;i++){const [s0,n0]=ring[(i+3)%4],[,n1]=ring[i];const rel=((a-s0)%360+360)%360;if(rel<=90){const p=rel/90;g[n0]=Math.cos(p*Math.PI/2);g[n1]=Math.sin(p*Math.PI/2);break}}
  const lin=10**((di>1?-6*Math.log2(di):0)/20);
  document.getElementById('meters').innerHTML=[1,2,3,4].map(n=>{const v=g[n]*lin;return `<div class="meter"><span>HP ${n}</span><span class="bar"><b style="width:${(v*100).toFixed(1)}%"></b></span><span>${v>0.001?(20*Math.log10(v)).toFixed(1)+' dB':'−∞'}</span></div>`}).join('');
  document.getElementById('adMsg').textContent=`/source/1/ad ${az.toFixed(1)} ${di.toFixed(1)}`;
  document.getElementById('az').value=az;document.getElementById('di').value=di;
  document.getElementById('azO').textContent=Math.round(az)+'°';document.getElementById('diO').textContent=di.toFixed(1)+' m'};
 document.getElementById('az').addEventListener('input',e=>{az=+e.target.value;draw()});
 document.getElementById('di').addEventListener('input',e=>{di=+e.target.value;draw()});
 const pt=e=>{const r=room.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*400-cx,y=(e.clientY-r.top)/r.height*400-cy;
  az=Math.round(Math.atan2(x,-y)*180/Math.PI);di=Math.min(3.2,Math.max(0.2,Math.round(Math.hypot(x,y)/R*20)/10));draw()};
 room.addEventListener('pointerdown',e=>{drag=true;room.setPointerCapture(e.pointerId);pt(e)});
 room.addEventListener('pointermove',e=>{if(drag)pt(e)});room.addEventListener('pointerup',()=>drag=false);
 draw();
}

/* ---------- adsr demo ---------- */
const env=document.getElementById('env');
if(env){
 const E={A:5,D:50,S:.5,R:200,M:500};
 const sim=()=>{const pts=[];let lv=0,ph='i',t0=0,st=0,gate=false;
  for(let t=0;t<=2000;t++){const g=Math.floor(t/E.M)%2===0;
   if(g&&!gate){ph='A';t0=t;st=lv}if(!g&&gate){ph='R';t0=t;st=lv}gate=g;const dt=t-t0;
   if(ph==='A'){lv=st+(1-st)*Math.min(1,dt/E.A);if(dt>=E.A){ph='D';t0=t}}
   else if(ph==='D'){lv=1+(E.S-1)*Math.min(1,dt/E.D);if(dt>=E.D)ph='S'}
   else if(ph==='S')lv=E.S;else if(ph==='R')lv=st*Math.max(0,1-dt/E.R);
   pts.push(lv)}return pts};
 const draw=()=>{const W=env.clientWidth,H=env.clientHeight,pl=30,pb=22,pt=8,iw=W-pl-6,ih=H-pb-pt,T=2000,p=sim();let s='';
  for(let k=0;k*E.M<T;k+=2)s+=`<rect x="${pl+k*E.M/T*iw}" y="${pt}" width="${Math.min(E.M,T-k*E.M)/T*iw}" height="${ih}" fill="var(--grid)"/>`;
  [0,.5,1].forEach(v=>{const y=pt+ih-v*ih;s+=`<line x1="${pl}" x2="${W-6}" y1="${y}" y2="${y}" stroke="var(--line)"/><text x="${pl-6}" y="${y+4}" text-anchor="end" font-size="11" fill="var(--mut)" font-family="JetBrains Mono,monospace">${v}</text>`});
  (W<520?[0,1000,2000]:[0,500,1000,1500,2000]).forEach(t=>{s+=`<text x="${pl+t/T*iw}" y="${H-5}" text-anchor="${t===0?'start':t===T?'end':'middle'}" font-size="11" fill="var(--mut)" font-family="JetBrains Mono,monospace">${t} ms</text>`});
  let d='';for(let t=0;t<=T;t+=2)d+=(t?'L':'M')+(pl+t/T*iw).toFixed(1)+' '+(pt+ih-p[t]*ih).toFixed(1);
  s+=`<path d="${d}" fill="none" stroke="var(--acc)" stroke-width="1.6"/>`;env.innerHTML=s};
 const envRO=new ResizeObserver(draw);envRO.observe(env);
 [['eA','A',' ms'],['eD','D',' ms'],['eS','S',''],['eR','R',' ms'],['eM','M',' ms']].forEach(([id,k,u])=>document.getElementById(id).addEventListener('input',e=>{
  E[k]=+e.target.value;document.getElementById(id+'O').textContent=E[k]+u;
  document.getElementById('adsrMsg').textContent=`adsr~ ${E.A} ${E.D} ${E.S} ${E.R} · metro ${E.M}`;draw()}));
}

/* ---------- checklist ---------- */
document.querySelectorAll('.try').forEach(ul=>{const key='emc-try-'+ul.dataset.key,bx=[...ul.querySelectorAll('input')];
 try{const s=JSON.parse(localStorage.getItem(key)||'[]');bx.forEach((b,i)=>b.checked=!!s[i])}catch(e){}
 bx.forEach(b=>b.addEventListener('change',()=>{try{localStorage.setItem(key,JSON.stringify(bx.map(x=>x.checked)))}catch(e){}}))});
}
