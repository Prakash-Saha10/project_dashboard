// app.js - single entry for UI behaviors (put in static/js/)
document.addEventListener('DOMContentLoaded', function() {
  // 1) Auto-add bootstrap classes to form fields if not present
  document.querySelectorAll('form').forEach(form=>{
    form.querySelectorAll('input[type="text"], input[type="email"], input[type="date"], input[type="search"], textarea').forEach(el=>{
      if(!el.classList.contains('form-control')) el.classList.add('form-control');
    });
    form.querySelectorAll('select').forEach(el=>{
      if(!el.classList.contains('form-select')) el.classList.add('form-select');
    });
  });

  // 2) Initialize Select2 if present
  if(window.jQuery && jQuery().select2){
    $('select').select2({ theme: 'bootstrap-5', width: '100%' });
  }

  // 3) Initialize datepicker
  if(window.jQuery && jQuery().datepicker){
    $('.datepicker').datepicker({ format:'yyyy-mm-dd', autoclose:true, todayHighlight:true });
  }

  // 4) Tooltips
  var t = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  t.map(function(el){ return new bootstrap.Tooltip(el); });

  // 5) Chart helpers (doughnut) - any canvas with data attributes
  document.querySelectorAll('canvas[data-chart="doughnut"]').forEach(canvas=>{
    try{
      const ctx = canvas.getContext('2d');
      const raw = JSON.parse(canvas.dataset.payload || "{}");
      new Chart(ctx, {
        type: 'doughnut',
        data: raw,
        options: { maintainAspectRatio: false, plugins: { legend:{ position:'bottom' } }, cutout: '70%' }
      });
    }catch(e){ console.warn('chart error', e); }
  });

  // 6) Notification WebSocket (uses ws:// or wss:// based on page)
  const scheme = (window.location.protocol === "https:") ? 'wss':'ws';
  try{
    const socket = new WebSocket(scheme + '://' + window.location.host + '/ws/notifications/');
    socket.onmessage = function(e){
      try{
        const data = JSON.parse(e.data);
        // update unread badge
        const badge = document.getElementById('unreadCount');
        if(badge){
          const n = parseInt(badge.textContent || '0') + 1;
          badge.textContent = n;
        }
        // prepend a small notification node (if dropdown exists)
        const list = document.getElementById('notificationList');
        if(list){
          const node = document.createElement('a');
          node.className = 'dropdown-item border-bottom notification-item unread';
          node.href = data.url || '#';
          node.innerHTML = '<div class="small text-truncate">'+ (data.message||'New update') +'</div><small class="text-muted">just now</small>';
          list.insertBefore(node, list.firstChild);
        }
      }catch(e){ console.warn(e); }
    };
  }catch(e){ console.warn('WS not available', e); }

});
