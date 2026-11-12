// Click-to-load YouTube player for real tracks.
// Shows a thumbnail first; the YouTube iframe (≈1MB, cookies) loads only when clicked,
// from youtube-nocookie.com. A plain search link is always kept as a fallback, because
// videos get removed. IDs come from window.TRANCE_VIDEOS (assets/videos.js), keyed "Artist — Title".
(() => {
  const searchUrl = q => 'https://www.youtube.com/results?search_query=' + encodeURIComponent(q);
  // YouTube refuses to embed into file:// pages (no referrer), so there we open YouTube instead.
  const canEmbed = location.protocol === 'http:' || location.protocol === 'https:';

  function el(tag, attrs, kids) {
    const n = document.createElement(tag);
    for (const k in attrs || {}) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else n.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(c => c && n.append(c));
    return n;
  }

  /** @param {{artist:string, title?:string, note?:string}} t */
  function player(t) {
    const key = t.title ? t.artist + ' — ' + t.title : t.artist;
    const label = t.title ? t.artist + ' – ' + t.title : t.artist;
    const v = (window.TRANCE_VIDEOS || {})[key];
    const box = el('figure', { class: 'video' });
    const search = el('a', { class: 'video-search', href: searchUrl(label), target: '_blank', rel: 'noopener', text: v ? 'לא עובד? חיפוש ב־YouTube' : 'חיפוש ב־YouTube' });

    if (v) {
      const frame = el('div', { class: 'video-frame' });
      const btn = el('button', { class: 'video-play', type: 'button', 'aria-label': 'נגן: ' + label }, [
        el('img', { src: 'https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg', alt: '', loading: 'lazy', decoding: 'async' }),
        el('span', { class: 'video-icon', 'aria-hidden': 'true' })
      ]);
      btn.addEventListener('click', () => {
        document.dispatchEvent(new CustomEvent('s2video:play'));
        if (!canEmbed) { window.open('https://www.youtube.com/watch?v=' + v.id, '_blank', 'noopener'); return; }
        const ifr = el('iframe', {
          src: 'https://www.youtube-nocookie.com/embed/' + v.id + '?autoplay=1&rel=0',
          title: label,
          allow: 'autoplay; encrypted-media; picture-in-picture; fullscreen',
          referrerpolicy: 'strict-origin-when-cross-origin'
        });
        frame.replaceChildren(ifr);
        ifr.focus();
      });
      frame.append(btn);
      box.append(frame);
    }

    box.append(el('figcaption', null, [
      el('span', { class: 'ltr video-name', text: label }),
      t.note ? el('span', { class: 'video-note', text: t.note }) : null,
      search
    ]));
    return box;
  }

  window.S2Video = { player };
})();
