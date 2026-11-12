// Viewer-selectable color palette for the S2 skin.
// Load in <head> without defer, so the saved palette applies before first paint (no flash).
// Any element with [data-palette-picker] gets filled with swatch buttons.
(() => {
  const KEY = 'trance-palette';
  // Swatch colors only. The real tokens live in assets/s2.css under :root[data-palette].
  const PALETTES = [
    { id: 'uv',    name: 'UV',          colors: ['#FF4FD8', '#3DDCF0', '#A6EE3B'] },
    { id: 'laser', name: 'לייזר',       colors: ['#C6FF3D', '#B58CFF', '#FF8AD8'] },
    { id: 's2',    name: 'S2 המקורי',   colors: ['#FF6B35', '#38B6D6', '#8BD346'] },
  ];
  const DEFAULT = 'uv';
  const root = document.documentElement;

  const read = () => { try { return localStorage.getItem(KEY); } catch { return null; } };
  const save = id => { try { localStorage.setItem(KEY, id); } catch { /* private mode: keep it for this visit only */ } };

  function apply(id) {
    if (!PALETTES.some(p => p.id === id)) id = DEFAULT;
    if (id === DEFAULT) delete root.dataset.palette; else root.dataset.palette = id;
    document.querySelectorAll('.swatch').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.id === id)));
    document.dispatchEvent(new CustomEvent('palettechange', { detail: id }));
    return id;
  }

  function buildPickers() {
    document.querySelectorAll('[data-palette-picker]').forEach(host => {
      host.classList.add('palettes');
      host.setAttribute('role', 'group');
      host.setAttribute('aria-label', 'פלטת צבעים');
      host.innerHTML = '<span class="lbl" aria-hidden="true">צבעים</span>';
      for (const p of PALETTES) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'swatch';
        b.dataset.id = p.id;
        b.title = p.name;
        b.setAttribute('aria-label', p.name);
        b.style.cssText = `--sw-a:${p.colors[0]};--sw-b:${p.colors[1]};--sw-c:${p.colors[2]}`;
        b.addEventListener('click', () => save(apply(p.id)));
        host.append(b);
      }
    });
    apply(read() || DEFAULT);
  }

  apply(read() || DEFAULT);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', buildPickers);
  else buildPickers();
})();
