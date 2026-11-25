{
const idx=JSON.parse(document.getElementById('idx').textContent);
const q=document.getElementById('q'),hits=document.getElementById('hits'),tg=document.getElementById('tags');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const norm=s=>String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
const all=[...new Set(idx.flatMap(s=>s.tags))].sort((a,b)=>a.localeCompare(b,'fr'));
const run=()=>{const v=norm(q.value.trim());
 tg.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',norm(b.textContent)===v));
 if(!v){hits.innerHTML='';return}
 const res=idx.map(s=>{const why=[...s.tags.filter(t=>norm(t).includes(v)),...s.objs.filter(o=>norm(o).includes(v))];
  return {s,why,ok:why.length||norm(s.t).includes(v)}}).filter(r=>r.ok);
 hits.innerHTML=res.length?res.map(({s,why})=>`<a class="row" href="${esc(s.h)}"><span class="d">${esc(s.d)}</span><span class="t">${esc(s.t)}</span><span class="c">${esc(s.c)} →</span>${why.length?`<span class="why">${why.map(esc).join(' · ')}</span>`:''}</a>`).join(''):'<p class="empty">Aucun cours pour « '+esc(q.value)+' ».</p>'};
tg.innerHTML=all.map(t=>`<button type="button" aria-pressed="false">${esc(t)}</button>`).join('');
tg.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;q.value=b.getAttribute('aria-pressed')==='true'?'':b.textContent;run()});
q.addEventListener('input',run);
const p=new URLSearchParams(location.search).get('q');if(p){q.value=p;run()}
}
