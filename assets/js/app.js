(function(){
  var C = window.NO_CONFIG || {};
  var isPh = function(u){ return !u || /REPLACE/.test(u); };
  function toast(msg){
    var t=document.getElementById('toast');
    if(!t){t=document.createElement('div');t.id='toast';t.className='toast';document.body.appendChild(t);}
    t.textContent=msg;t.classList.add('show');clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('show')},3200);
  }
  function resolve(kind, course){
    if(kind==='channel') return C.TELEGRAM_CHANNEL_URL;
    if(kind==='bot') return C.TELEGRAM_BOT_URL;
    if(kind==='contact') return C.CONTACT_URL;
    if(kind==='pay'){ var p=C.PAY||{}; return (course&&p[course])||p['default']; }
    var soc={youtube:'YOUTUBE_URL',instagram:'INSTAGRAM_URL',tiktok:'TIKTOK_URL',vk:'VK_URL'};
    if(soc[kind]) return C[soc[kind]];
    return '';
  }
  document.querySelectorAll('[data-link]').forEach(function(a){
    var kind=a.getAttribute('data-link'), url=resolve(kind,a.getAttribute('data-course'));
    if(a.hasAttribute('data-social')){ if(!url){a.remove();return;} }
    if(isPh(url)){
      a.setAttribute('href','#');
      a.addEventListener('click',function(e){e.preventDefault();
        toast(kind==='pay'?'Оплата подключается — напишите нам в Telegram, и мы забронируем место.':'Telegram-канал запускается — ссылка появится здесь совсем скоро.');});
    } else { a.setAttribute('href',url); a.setAttribute('target','_blank'); a.setAttribute('rel','noopener'); }
  });
  document.querySelectorAll('[data-keyword]').forEach(function(el){ el.textContent=C.KEYWORD||'ИИ'; });

  // меню
  var b=document.querySelector('.burger'), n=document.querySelector('.nav');
  if(b&&n) b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});

  // появление при скролле
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  } else document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});

  // лента «Новое каждый день»
  var feed=document.getElementById('feed');
  if(feed){
    var limit=parseInt(feed.getAttribute('data-limit')||'0',10), root=feed.getAttribute('data-root')||'';
    fetch(root+'data/feed.json?v='+Date.now()).then(function(r){return r.json()}).then(function(d){
      var items=(d.items||[]).slice().sort(function(a,b){return a.date<b.date?1:-1});
      if(limit) items=items.slice(0,limit);
      var esc=function(s){return String(s||'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
      var fmt=function(s){var m=['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];var p=s.split('-');return parseInt(p[2],10)+' '+m[parseInt(p[1],10)-1]+' '+p[0];};
      feed.innerHTML=items.map(function(it){
        return '<article class="fcard reveal in"><div class="fmeta"><span class="tag">'+esc(it.tag)+'</span><time datetime="'+esc(it.date)+'">'+fmt(it.date)+'</time></div>'+
        '<h3>'+esc(it.title)+'</h3><p>'+esc(it.text)+'</p>'+
        (it.how?'<p class="how"><b>Как применить:</b> '+esc(it.how)+'</p>':'')+
        (it.region?'<p class="region">Доступность: '+esc(it.region)+'</p>':'')+
        '<div class="factions">'+(it.video_url?'<a class="btn sm" href="'+esc(it.video_url)+'" target="_blank" rel="noopener">▶ Смотреть видео</a>':'')+
        '<a class="src" href="'+esc(it.source_url)+'" target="_blank" rel="noopener">Источник: '+esc(it.source_name)+' ↗</a></div></article>';
      }).join('');
    }).catch(function(){feed.innerHTML='<p class="muted">Не удалось загрузить ленту. Обновите страницу.</p>'});
  }
})();
