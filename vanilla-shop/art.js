// Natural Vanilla Tea box artwork.
// Every panel is drawn in millimetres. All type is converted to outlines with opentype.js,
// so the same SVG renders identically in the browser, in three.js textures and in Illustrator.
(function (root) {
  const VS = {};
  const MM = 72 / 25.4; // points per millimetre

  // ---------------------------------------------------------------------------
  // Geometry measured from the supplied dieline (points, y down, artboard origin).
  // `panel` = fold-to-fold face. `region` = the artwork/bleed area used in the source file.
  VS.ARTBOARD = { w: 1194.94, h: 1052.97 };
  const R = (x0, y0, x1, y1) => ({ x: x0, y: y0, w: x1 - x0, h: y1 - y0 });
  VS.PANELS = {
    front:   { panel: R(145.46, 390.86, 393.94, 631.07),  region: R(141.258, 391.242, 393.320, 630.828) },
    sideA:   { panel: R(393.94, 390.86, 633.68, 631.07),  region: R(393.035, 250.227, 634.207, 656.613) },
    back:    { panel: R(633.68, 390.86, 881.95, 631.07),  region: R(632.051, 391.246, 882.355, 630.699) },
    sideB:   { panel: R(881.95, 390.86, 1122.45, 631.07), region: R(882.137, 250.227, 1123.309, 656.613) },
    top:     { panel: R(145.50, 149.85, 393.53, 390.72),  region: R(142.715, 89.582, 393.961, 390.723) },
    inner:   { panel: R(145.50, 630.22, 393.53, 871.09),  region: R(142.715, 628.051, 393.961, 929.191) },
    bottom:  { panel: R(633.68, 631.07, 881.70, 870.00),  region: R(629.184, 629.949, 881.703, 881.480) },
  };
  VS.mm = (pt) => pt / MM;
  // Box size for the 3D model (mm): width x height x depth.
  VS.BOX = { w: VS.mm(VS.PANELS.front.panel.w), h: VS.mm(VS.PANELS.front.panel.h), d: VS.mm(VS.PANELS.sideA.panel.w) };

  // ---------------------------------------------------------------------------
  // Colourways. Forest keeps the existing brand green (#143A1D) and cream (#FEF8E9) from the source file.
  const PLATE_FRAME = { paper: '#FEF8E9', frame: '#143A1D', frameInk: '#FEF8E9', frameSub: '#B9C7A2', frameAccent: '#D3DD7C' };
  VS.COLORWAYS = {
    ceylon: {
      name: 'Ceylon plate', design: 'plate', bg: '#143A1D', ink: '#FEF8E9', sub: '#C7D2AE', accent: '#D3DD7C', glow: '#EBC86A',
      leafA: '#6E9B45', leafB: '#43733A', vine: '#9DBE5C', sepal: '#DDE3A0', petal: '#EEF0C2',
      lip: '#FFF7D2', throat: '#E7BE4A', pod: '#3A2416', podHi: '#8A5E3E', shadow: '#0A2311',
      cut: '#143A1D', badge: '#D3DD7C', badgeInk: '#143A1D', twine: '#FEF8E9', ...PLATE_FRAME,
    },
    ceylonCream: {
      name: 'Ceylon plate, cream sides', design: 'plate', bg: '#FEF8E9', ink: '#143A1D', sub: '#55704C', accent: '#5E8C3A', glow: '#E7BE4A',
      leafA: '#5E8C3A', leafB: '#2F5E2A', vine: '#7EA34A', sepal: '#C9D57A', petal: '#DCE3A0',
      lip: '#F5E296', throat: '#D6A436', pod: '#3A2416', podHi: '#8A5E3E', shadow: '#E4DAC0',
      cut: '#FEF8E9', badge: '#143A1D', badgeInk: '#FEF8E9', twine: '#143A1D', ...PLATE_FRAME,
    },
    forest: {
      name: 'Forest', bg: '#143A1D', ink: '#FEF8E9', sub: '#C7D2AE', accent: '#D3DD7C', glow: '#EBC86A',
      leafA: '#6E9B45', leafB: '#43733A', vine: '#9DBE5C', sepal: '#DDE3A0', petal: '#EEF0C2',
      lip: '#FFF7D2', throat: '#E7BE4A', pod: '#3A2416', podHi: '#8A5E3E', shadow: '#0A2311',
      cut: '#143A1D', badge: '#D3DD7C', badgeInk: '#143A1D', twine: '#FEF8E9',
    },
    cream: {
      name: 'Cream', bg: '#FEF8E9', ink: '#143A1D', sub: '#55704C', accent: '#5E8C3A', glow: '#E7BE4A',
      leafA: '#5E8C3A', leafB: '#2F5E2A', vine: '#7EA34A', sepal: '#C9D57A', petal: '#DCE3A0',
      lip: '#F5E296', throat: '#D6A436', pod: '#3A2416', podHi: '#8A5E3E', shadow: '#E4DAC0',
      cut: '#FEF8E9', badge: '#143A1D', badgeInk: '#FEF8E9', twine: '#143A1D',
    },
    lime: {
      name: 'Lime', bg: '#D5DE80', ink: '#143A1D', sub: '#3D5A2E', accent: '#8A4B2A', glow: '#FEF8E9',
      leafA: '#3F7A33', leafB: '#1F4F24', vine: '#2F6A2A', sepal: '#FEF8E9', petal: '#FFFCEF',
      lip: '#FFF0B8', throat: '#E2B43E', pod: '#3A2416', podHi: '#8A5E3E', shadow: '#AEB85E',
      cut: '#D5DE80', badge: '#143A1D', badgeInk: '#D5DE80', twine: '#143A1D',
    },
  };

  // ---------------------------------------------------------------------------
  // Fonts + outlined text
  let F = null; // { display, italic, sans, bold, mono } opentype.Font objects
  VS.setFonts = (fonts) => { F = fonts; };

  const n = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;

  function measure(font, str, size, track = 0) {
    const glyphs = font.stringToGlyphs(str);
    const scale = size / font.unitsPerEm;
    let w = 0;
    glyphs.forEach((g, i) => {
      w += g.advanceWidth * scale;
      if (i < glyphs.length - 1) w += font.getKerningValue(g, glyphs[i + 1]) * scale + track * size;
    });
    return w;
  }
  VS.measure = (key, str, size, track) => measure(F[key], str, size, track);

  // Returns a path `d` for a line of text. anchor: start | middle | end. track in em.
  function textD(font, str, size, x, y, anchor = 'start', track = 0) {
    const glyphs = font.stringToGlyphs(str);
    const scale = size / font.unitsPerEm;
    const w = measure(font, str, size, track);
    let cx = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
    let d = '';
    glyphs.forEach((g, i) => {
      d += g.getPath(cx, y, size).toPathData(3);
      cx += g.advanceWidth * scale;
      if (i < glyphs.length - 1) cx += font.getKerningValue(g, glyphs[i + 1]) * scale + track * size;
    });
    return d;
  }
  const T = (key, str, size, x, y, fill, o = {}) => {
    const d = textD(F[key], o.upper ? str.toUpperCase() : str, size, x, y, o.anchor, o.track || 0);
    const extra = o.opacity != null ? ` opacity="${o.opacity}"` : '';
    const tr = o.transform ? ` transform="${o.transform}"` : '';
    return `<path d="${d}" fill="${fill}"${extra}${tr}/>`;
  };

  // Text set around a circle, reading clockwise from the top.
  function ringText(key, str, size, cx, cy, r, fill, track = 0) {
    const font = F[key];
    const glyphs = font.stringToGlyphs(str);
    const scale = size / font.unitsPerEm;
    const total = measure(font, str, size, track);
    const circ = 2 * Math.PI * r;
    const spread = circ / total; // stretch so the string closes the circle
    let s = 0, out = '';
    glyphs.forEach((g, i) => {
      const adv = g.advanceWidth * scale;
      const mid = (s + adv / 2) * spread;
      const a = (mid / r) * 180 / Math.PI;
      const d = g.getPath(-adv / 2, 0, size).toPathData(3);
      if (d) out += `<path d="${d}" fill="${fill}" transform="translate(${n(cx)} ${n(cy)}) rotate(${n(a)}) translate(0 ${n(-r)})"/>`;
      s += adv + (i < glyphs.length - 1 ? font.getKerningValue(g, glyphs[i + 1]) * scale + track * size : 0);
    });
    return out;
  }

  // ---------------------------------------------------------------------------
  // Seeded randomness so every render matches the export.
  function rng(seed) {
    let t = seed >>> 0;
    return () => {
      t += 0x6D2B79F5;
      let r = Math.imul(t ^ (t >>> 15), 1 | t);
      r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
      return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Grain glow: a vector stipple whose density falls off from the centre (prints as solid dots).
  function stipple(cx, cy, rx, ry, count, fill, seed, rMin = 0.14, rMax = 0.32) {
    const rand = rng(seed);
    let d = '', placed = 0, guard = 0;
    while (placed < count && guard < count * 30) {
      guard++;
      const a = rand() * Math.PI * 2, t = Math.sqrt(rand());
      const fall = Math.pow(1 - t, 1.7);
      if (rand() > fall) continue;
      const x = cx + Math.cos(a) * t * rx, y = cy + Math.sin(a) * t * ry;
      const r = rMin + (rMax - rMin) * rand() * (0.5 + fall * 0.5);
      d += `M${n(x - r)} ${n(y)}a${n(r)} ${n(r)} 0 1 0 ${n(2 * r)} 0a${n(r)} ${n(r)} 0 1 0 ${n(-2 * r)} 0`;
      placed++;
    }
    return `<path d="${d}" fill="${fill}"/>`;
  }

  // ---------------------------------------------------------------------------
  // Botanical shapes (cut-paper style: flat fills, a lifted shadow, negative-space cuts)

  // Lanceolate shape from the origin pointing up (-y).
  const blade = (len, wid, bend = 0) =>
    `M0 0C${n(wid * 0.95)} ${n(-len * 0.18)} ${n(wid * 1.05 + bend * 0.5)} ${n(-len * 0.62)} ${n(bend)} ${n(-len)}` +
    `C${n(-wid * 0.95 + bend * 0.5)} ${n(-len * 0.62)} ${n(-wid * 0.95)} ${n(-len * 0.18)} 0 0Z`;

  function leaf(x, y, angle, len, c, fill, o = {}) {
    const wid = len * (o.w || 0.3), bend = o.bend || 0;
    const tr = `translate(${n(x)} ${n(y)}) rotate(${n(angle)})`;
    return `<g transform="${tr}">` +
      `<path d="${blade(len, wid, bend)}" fill="${c.shadow}" transform="translate(0.55 0.75)"/>` +
      `<path d="${blade(len, wid, bend)}" fill="${fill}"/>` +
      `<path d="M0 ${n(-len * 0.1)}Q${n(bend * 0.25)} ${n(-len * 0.5)} ${n(bend * 0.85)} ${n(-len * 0.9)}" fill="none" stroke="${c.cut}" stroke-width="0.5" stroke-linecap="round"/>` +
      `</g>`;
  }

  // Vanilla planifolia flower in three-quarter view: 3 narrow sepals, 2 petals,
  // and the rolled trumpet lip (labellum) with a ruffled mouth and a yellow throat.
  function orchid(x, y, s, rot, c) {
    const parts = [
      // [angle, length, width, bend, colour]
      [-6, 13.2, 2.5, 1.4, c.sepal],
      [128, 12.6, 2.5, -1.6, c.sepal],
      [-132, 12.4, 2.5, 1.8, c.sepal],
      [56, 11.8, 2.25, 1.6, c.petal],
      [-62, 11.6, 2.25, -1.4, c.petal],
    ];
    const blades = (fill) => parts.map(([a, l, w, b, col]) =>
      `<path d="${blade(l, w, b)}" fill="${fill || col}" transform="rotate(${a})"/>`).join('');
    const lipD = 'M-2.3 -0.4C-2.7 3.2 -4.5 6.3 -5.5 8.5Q-4.4 10.3 -3.1 9.3Q-2.1 10.7 -0.9 9.6Q0 10.9 0.9 9.6Q2.1 10.7 3.1 9.3Q4.4 10.3 5.5 8.5C4.5 6.3 2.7 3.2 2.3 -0.4Z';
    const lip = `<g transform="rotate(12)">` +
      `<path d="${lipD}" fill="${c.shadow}" transform="translate(0.5 0.7)"/>` +
      `<path d="${lipD}" fill="${c.lip}"/>` +
      `<ellipse cx="0" cy="8.35" rx="4.2" ry="1.25" fill="${c.throat}"/>` +
      `<path d="M0 1.6L-1.5 7.5M0 1.4L0 7.7M0 1.6L1.5 7.5" stroke="${c.throat}" stroke-width="0.42" stroke-linecap="round" fill="none"/>` +
      `<path d="M-0.75 -1.6h1.5v3.6a0.75 0.75 0 0 1 -1.5 0Z" fill="${c.petal}"/>` +
      `</g>`;
    return `<g transform="translate(${n(x)} ${n(y)}) rotate(${n(rot)}) scale(${n(s)})">` +
      `<g transform="translate(0.6 0.8)">${blades(c.shadow)}</g>${blades()}${lip}</g>`;
  }

  function bud(x, y, angle, s, c) {
    return `<g transform="translate(${n(x)} ${n(y)}) rotate(${n(angle)}) scale(${n(s)})">` +
      `<path d="${blade(6, 1.5, 0.4)}" fill="${c.shadow}" transform="translate(0.4 0.5)"/>` +
      `<path d="${blade(6, 1.5, 0.4)}" fill="${c.sepal}"/>` +
      `<path d="${blade(2.6, 1.4, 0)}" fill="${c.leafA}"/></g>`;
  }

  // Cured vanilla pod along +x, with a highlight ridge and wrinkle ticks.
  function pod(x, y, angle, len, c, seed = 1, w = 1.25) {
    const d = `M0 0C${n(len * 0.18)} ${n(-w)} ${n(len * 0.8)} ${n(-w * 1.1)} ${n(len)} ${n(-w * 0.2)}` +
      `C${n(len * 0.8)} ${n(w * 0.85)} ${n(len * 0.18)} ${n(w)} 0 0Z`;
    const rand = rng(seed);
    let ticks = '';
    for (let i = 0; i < 9; i++) {
      const t = 0.12 + i * 0.09 + rand() * 0.03, yy = (rand() - 0.5) * w * 0.8;
      ticks += `M${n(len * t)} ${n(yy - 0.25)}l${n(0.9 + rand())} ${n(0.18)}`;
    }
    return `<g transform="translate(${n(x)} ${n(y)}) rotate(${n(angle)})">` +
      `<path d="${d}" fill="${c.shadow}" transform="translate(0.5 0.7)"/>` +
      `<path d="${d}" fill="${c.pod}"/>` +
      `<path d="M${n(len * 0.06)} ${n(-w * 0.3)}C${n(len * 0.3)} ${n(-w * 0.78)} ${n(len * 0.72)} ${n(-w * 0.84)} ${n(len * 0.93)} ${n(-w * 0.35)}" stroke="${c.podHi}" stroke-width="0.38" fill="none" stroke-linecap="round"/>` +
      `<path d="${ticks}" stroke="${c.podHi}" stroke-width="0.22" opacity="0.7" fill="none" stroke-linecap="round"/>` +
      `</g>`;
  }

  // Two cured pods tied with twine.
  function podBundle(x, y, angle, len, c) {
    return `<g transform="translate(${n(x)} ${n(y)}) rotate(${n(angle)})">` +
      pod(0, 0.6, 3.5, len, c, 3) + pod(0, -0.6, -2.5, len * 0.97, c, 7) +
      `<g transform="translate(${n(len * 0.46)} 0)" fill="none" stroke="${c.twine}" stroke-width="0.4" stroke-linecap="round">` +
      `<path d="M-0.6 -2.6Q0.6 0 -0.6 2.6M0.7 -2.6Q1.9 0 0.7 2.6"/>` +
      `<path d="M0 2.4q2.4 1.4 3.4 4.2M0.4 2.4q-0.4 2.6 -2 4.6"/></g></g>`;
  }

  function vine(d, c, w = 1.5) {
    return `<path d="${d}" fill="none" stroke="${c.shadow}" stroke-width="${w}" stroke-linecap="round" transform="translate(0.5 0.7)"/>` +
      `<path d="${d}" fill="none" stroke="${c.vine}" stroke-width="${w}" stroke-linecap="round"/>`;
  }

  // Round brand stamp.
  function stamp(cx, cy, r, c, text, o = {}) {
    const fill = o.fill || c.badge, ink = o.ink || c.badgeInk;
    return `<g class="vs-spin" data-cx="${n(cx)}" data-cy="${n(cy)}">` +
      `<circle cx="${n(cx)}" cy="${n(cy)}" r="${n(r)}" fill="${fill}"/>` +
      ringText('bold', text, r * 0.21, cx, cy, r * 0.71, ink, 0.06) + `</g>` +
      (o.center === false ? '' : crossedPods(cx, cy, r * 0.5, ink, fill));
  }

  // Stamp centre: two cured pods crossed and tied.
  function crossedPods(cx, cy, len, ink, fill) {
    const k = { pod: ink, podHi: fill, shadow: fill };
    const w = len * 0.06;
    return `<g transform="translate(${n(cx)} ${n(cy)})">` +
      pod(-len / 2, 0, 0, len, k, 9, w).replace('<g transform="', `<g transform="rotate(-38) `) +
      pod(-len / 2, 0, 0, len, k, 4, w).replace('<g transform="', `<g transform="rotate(38) `) +
      `<circle r="${n(len * 0.075)}" fill="${fill}"/><circle r="${n(len * 0.045)}" fill="${ink}"/></g>`;
  }

  const rect = (x, y, w, h, fill, o = '') => `<rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" fill="${fill}"${o}/>`;
  const rule = (x1, y, x2, col, w = 0.25) => `<path d="M${n(x1)} ${n(y)}H${n(x2)}" stroke="${col}" stroke-width="${w}"/>`;

  // Dashed slot for artwork that must come from the client (licensed or official files).
  function slot(x, y, w, h, label, c, lines = 1) {
    const out = [`<rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" rx="1.2" fill="none" stroke="${c.sub}" stroke-width="0.25" stroke-dasharray="0.8 0.6"/>`];
    const parts = label.split('\n');
    parts.forEach((p, i) => out.push(T('mono', p, 1.35, x + w / 2, y + h / 2 + 0.5 + (i - (parts.length - 1) / 2) * 1.9, c.sub, { anchor: 'middle', upper: true, track: 0.04 })));
    return out.join('');
  }

  // ---------------------------------------------------------------------------
  // Panels. Each returns SVG content drawn in mm with the panel's top-left at 0,0.
  // `bleed` fills well past the fold so clipping to the source regions leaves no gaps.

  function bgFill(w, h, c, bleed = 60) { return rect(-bleed, -bleed, w + bleed * 2, h + bleed * 2, c.bg); }

  VS.front = (c, w, h) => {
    const P = [];
    P.push(bgFill(w, h, c));
    P.push(stipple(55, 30, 30, 27, 1100, c.glow, 11));
    // vine entering from the top edge, with an aerial root
    P.push(vine('M76 -6C73 6 73 14 68 22C63 31 60 41 67 51C72 58 82 60 94 63', c));
    P.push(vine('M66 45c3 1 4 4 3 7s1 5 3 6', c, 0.45));
    P.push(leaf(71.5, 12, 38, 18, c, c.leafA, { bend: 2.4 }));
    P.push(leaf(63.5, 36, -104, 15, c, c.leafB, { bend: -2 }));
    P.push(leaf(72, 55.5, 112, 14, c, c.leafA, { bend: 1.8 }));
    // ovary/stalk from vine to flower, buds
    P.push(vine('M67.5 23.5C63 24 59 25 55 28', c, 0.9));
    P.push(bud(64, 22, -28, 1, c));
    P.push(bud(66.5, 25.5, 30, 0.85, c));
    P.push(podBundle(32.5, 57.5, -15, 50, c));
    P.push(orchid(51, 29, 1.18, -8, c));
    // stamp
    P.push(stamp(38.5, 12.5, 7.4, c, 'VANILLA WAS NEVER PLAIN • '));
    // vertical wordmark
    const size = 26.5;
    const vw = measure(F.display, 'Vanilla', size);
    const yStart = (h + vw) / 2;
    P.push(T('display', 'Vanilla', size, 0, 0, c.ink, { transform: `translate(25.4 ${n(yStart)}) rotate(-90)` }));
    // product block
    P.push(T('bold', 'Natural Vanilla Tea', 3.15, 31.5, 67.4, c.ink, { upper: true, track: 0.045 }));
    P.push(rule(31.5, 70.4, w - 5, c.ink));
    P.push(T('mono', '12 tea bags', 1.75, 31.5, 74.6, c.ink, { upper: true, track: 0.06 }));
    P.push(T('mono', 'Net wt 24 g', 1.75, (31.5 + w - 5) / 2 + 2, 74.6, c.ink, { upper: true, track: 0.06, anchor: 'middle' }));
    P.push(T('mono', 'Nº 01', 1.75, w - 5, 74.6, c.ink, { upper: true, track: 0.06, anchor: 'end' }));
    P.push(T('italic', 'The Vanilla Shop, Battaramulla', 2.7, 31.5, 80.2, c.sub));
    return P.join('');
  };

  VS.back = (c, w, h) => {
    const P = [];
    P.push(bgFill(w, h, c));
    P.push(stipple(74, 40, 16, 40, 520, c.glow, 21));
    // a single upright pod and a flower at its head
    P.push(pod(76.5, 79, -92, 64, c, 5, 1.45));
    P.push(leaf(77, 30, 26, 13, c, c.leafA, { bend: 1.6 }));
    P.push(leaf(75.5, 48, -28, 11, c, c.leafB, { bend: -1.4 }));
    P.push(orchid(74, 14.5, 0.92, 8, c));
    const s = 13.2;
    P.push(T('display', 'Vanilla', s, 6, 21.5, c.ink));
    P.push(T('display', 'was never', s, 6, 35.5, c.ink));
    P.push(T('italic', 'plain.', s * 1.08, 6, 50, c.accent));
    const body = ['The delicate sweetness of natural vanilla', 'unfolds through warm, comforting notes', 'and a smooth, mellow aroma.'];
    body.forEach((l, i) => P.push(T('sans', l, 2.35, 6, 61 + i * 3.6, c.ink, { opacity: 0.88 })));
    P.push(rule(6, 73.8, 60, c.ink));
    P.push(T('mono', 'Natural vanilla tea', 1.7, 6, 78, c.ink, { upper: true, track: 0.06 }));
    P.push(T('mono', '12 × 2 g', 1.7, 60, 78, c.ink, { upper: true, track: 0.06, anchor: 'end' }));
    return P.join('');
  };

  function iconCup(cx, cy, c) {
    return `<g transform="translate(${n(cx)} ${n(cy)})">` +
      `<circle r="6.2" fill="${c.badge}"/>` +
      `<path d="M-3.4 -1.2h6v2.6a3 3 0 0 1 -6 0Z" fill="${c.badgeInk}"/>` +
      `<path d="M2.6 -0.6a1.5 1.5 0 0 1 0 2.8" fill="none" stroke="${c.badgeInk}" stroke-width="0.6"/>` +
      `<path d="M-1.6 -2.4q-0.8 -1.2 0 -2.2M0.4 -2.4q-0.8 -1.2 0 -2.2" fill="none" stroke="${c.badgeInk}" stroke-width="0.45" stroke-linecap="round"/></g>`;
  }
  function iconTimer(cx, cy, c) {
    return `<g transform="translate(${n(cx)} ${n(cy)})">` +
      `<circle r="6.2" fill="${c.badge}"/>` +
      `<circle r="3.3" fill="none" stroke="${c.badgeInk}" stroke-width="0.6"/>` +
      `<path d="M0 0V-2.2M0 0L1.5 1" stroke="${c.badgeInk}" stroke-width="0.55" stroke-linecap="round"/>` +
      `<path d="M-0.8 -4.2h1.6" stroke="${c.badgeInk}" stroke-width="0.6" stroke-linecap="round"/></g>`;
  }
  function iconIce(cx, cy, c) {
    return `<g transform="translate(${n(cx)} ${n(cy)})">` +
      `<circle r="6.2" fill="${c.badge}"/>` +
      `<rect x="-3.2" y="-2.2" width="3.6" height="3.6" rx="0.6" fill="${c.badgeInk}" transform="rotate(-12)"/>` +
      `<rect x="0" y="-0.4" width="3.2" height="3.2" rx="0.6" fill="none" stroke="${c.badgeInk}" stroke-width="0.55" transform="rotate(14)"/></g>`;
  }

  VS.sideA = (c, w, h) => {
    const P = [];
    P.push(bgFill(w, h, c));
    P.push(T('italic', 'How to brew', 7.4, 6, 15, c.ink));
    P.push(T('mono', '2 g per tea bag', 1.7, w - 6, 15, c.sub, { upper: true, track: 0.06, anchor: 'end' }));
    P.push(rule(6, 19, w - 6, c.ink));
    const rows = [
      [iconCup, '150 ml', 'One tea bag in hot water'],
      [iconTimer, '5 min', 'Steep, then lift the bag out'],
      [iconIce, 'Over ice', 'Let it cool and pour over ice'],
    ];
    rows.forEach(([icon, big, small], i) => {
      const y = 31 + i * 17;
      P.push(icon(13, y, c));
      P.push(T('display', big, 7.2, 23.5, y + 1.2, c.ink));
      P.push(T('sans', small, 2.2, 23.5, y + 5.4, c.sub));
      if (i < 2) P.push(rule(23.5, y + 9.5, w - 6, c.ink, 0.15));
    });
    if (c.design !== 'plate') {
      P.push(leaf(w - 9, h - 4, -38, 12, c, c.leafA, { bend: -1.4 }));
      P.push(leaf(w - 7, h - 3, 18, 10, c, c.leafB, { bend: 1.2 }));
    }
    return P.join('');
  };

  VS.sideB = (c, w, h) => {
    const P = [];
    P.push(bgFill(w, h, c));
    P.push(T('display', 'Naturally aromatic', 5.6, 6, 13.5, c.ink));
    const story = ['A beautifully balanced infusion that celebrates', 'the pure essence of vanilla, creating a soothing,', 'memorable experience in every cup.'];
    story.forEach((l, i) => P.push(T('sans', l, 2.15, 6, 20 + i * 3.3, c.ink, { opacity: 0.88 })));
    const rows = [
      ['Ingredients', ['To be confirmed before print']],
      ['Net weight', ['24 g · 12 tea bags × 2 g']],
      ['Packed for', ['The Vanilla Shop', '253 Koswatta Road, Battaramulla, Sri Lanka']],
      ['Batch / Best before', ['See base of box']],
    ];
    let y = 33;
    rows.forEach(([k, vals]) => {
      P.push(rule(6, y, w - 6, c.ink, 0.15));
      P.push(T('mono', k, 1.55, 6, y + 3.2, c.sub, { upper: true, track: 0.06 }));
      vals.forEach((v, j) => P.push(T('sans', v, 2.05, 31, y + 3.2 + j * 3, k === 'Ingredients' ? c.accent : c.ink)));
      y += 4.6 + vals.length * 3;
    });
    P.push(slot(6, h - 16, 16, 11, 'Ceylon Tea\nlion logo', c));
    P.push(slot(24, h - 16, 18, 11, 'Agro Ventures\nlogo', c));
    P.push(slot(w - 30, h - 16, 24, 11, 'EAN-13\nbarcode', c));
    return P.join('');
  };

  VS.top = (c, w, h) => {
    const P = [];
    P.push(bgFill(w, h, c, 80));
    P.push(stipple(w / 2, h / 2, 36, 36, 900, c.glow, 31));
    P.push(stamp(w / 2, h / 2, 23, c, 'THE VANILLA SHOP • NATURAL VANILLA TEA • '));
    return P.join('');
  };

  VS.bottom = (c, w, h) => {
    const P = [];
    P.push(bgFill(w, h, c));
    P.push(stamp(w / 2, h / 2 - 6, 16, c, 'THE VANILLA SHOP • BATTARAMULLA • '));
    P.push(T('italic', 'Vanilla was never plain.', 4.2, w / 2, h / 2 + 20, c.ink, { anchor: 'middle' }));
    P.push(T('mono', 'Batch ________   Best before ________', 1.6, w / 2, h / 2 + 27, c.sub, { anchor: 'middle', upper: true, track: 0.05 }));
    return P.join('');
  };

  VS.inner = (c, w, h) => bgFill(w, h, c, 80) + stipple(w / 2, h * 0.45, 30, 30, 500, c.glow, 41);

  // ---------------------------------------------------------------------------
  // "Ceylon plate" design: George De Alwis's watercolour of Vanilla planifolia
  // (public domain, Wikimedia Commons), cleaned so its paper matches the brand cream.
  let IMG = {};
  VS.setImages = (images) => { IMG = images; };
  const PLATE_CREDIT = 'Vanilla planifolia · watercolour by George De Alwis, Ceylon';

  // Draws the plate scaled to `pw` mm wide with its top-left at x, y (plate fractions crop it).
  function plateImage(x, y, pw, crop = [0, 0, 1, 1]) {
    const p = IMG.plate;
    const cw = (crop[2] - crop[0]) * p.w, ch = (crop[3] - crop[1]) * p.h;
    const s = pw / cw;
    return `<image href="${p.href}" width="${p.w}" height="${p.h}" preserveAspectRatio="none" ` +
      `transform="translate(${n(x)} ${n(y)}) scale(${n(s, 6)}) translate(${n(-crop[0] * p.w)} ${n(-crop[1] * p.h)})"/>`;
  }
  const plateHeight = (pw, crop = [0, 0, 1, 1]) => pw * ((crop[3] - crop[1]) * IMG.plate.h) / ((crop[2] - crop[0]) * IMG.plate.w);

  const frontPlate = (c, w, h) => {
    const P = [], spine = 27, band = 66.5;
    P.push(rect(-60, -60, w + 120, h + 120, c.paper));
    // Painting in a cream window, framed by a forest spine and band like a picture mount.
    const pw = 61;
    P.push(plateImage(w + 0.3 - pw, -1.5, pw));
    P.push(rect(-60, -60, spine + 60, h + 120, c.frame));
    P.push(rect(spine, band, w + 60, h + 60, c.frame));
    P.push(rule(spine, band, w + 60, c.frameAccent, 0.5));
    const size = 25;
    const vw = measure(F.display, 'Vanilla', size);
    P.push(T('display', 'Vanilla', size, 0, 0, c.frameInk, { transform: `translate(24.2 ${n((h + vw) / 2)}) rotate(-90)` }));
    P.push(T('italic', 'Natural Vanilla Tea', 5.6, spine + 4.5, band + 7.6, c.frameInk));
    P.push(T('mono', '12 tea bags', 1.7, spine + 4.5, band + 12.6, c.frameSub, { upper: true, track: 0.06 }));
    P.push(T('mono', 'Net wt 24 g', 1.7, (spine + w) / 2 + 3, band + 12.6, c.frameSub, { upper: true, track: 0.06, anchor: 'middle' }));
    P.push(T('mono', 'Nº 01', 1.7, w - 4.5, band + 12.6, c.frameSub, { upper: true, track: 0.06, anchor: 'end' }));
    P.push(T('mono', 'Painted in Ceylon', 1.3, w - 2.2, band - 2.2, c.frame, { upper: true, track: 0.08, anchor: 'end', opacity: 0.7 }));
    return P.join('');
  };

  const backPlate = (c, w, h) => {
    const P = [];
    P.push(rect(-60, -60, w + 120, h + 120, c.frame));
    // Arched window onto the flowers.
    const ax = 47, aw = w - ax - 5, ay = 6, ah = 56, r = aw / 2;
    const arch = `M${n(ax)} ${n(ay + ah)}V${n(ay + r)}A${n(r)} ${n(r)} 0 0 1 ${n(ax + aw)} ${n(ay + r)}V${n(ay + ah)}Z`;
    const crop = [0.5, 0, 1, 0.56];
    const ph = plateHeight(aw, crop);
    P.push(`<clipPath id="arch-${c.id}"><path d="${arch}"/></clipPath>`);
    P.push(`<path d="${arch}" fill="${c.paper}"/>`);
    P.push(`<g clip-path="url(#arch-${c.id})">${plateImage(ax, ay + ah - ph, aw, crop)}</g>`);
    P.push(T('mono', 'George De Alwis, Ceylon', 1.35, ax + aw / 2, ay + ah + 4.2, c.frameSub, { anchor: 'middle', upper: true, track: 0.07 }));
    const s = 8.8;
    P.push(T('display', 'Vanilla', s, 6, 17, c.frameInk));
    P.push(T('display', 'was never', s, 6, 27.5, c.frameInk));
    P.push(T('italic', 'plain.', s * 1.08, 6, 38.5, c.frameAccent));
    const body = ['The delicate sweetness of natural', 'vanilla unfolds through warm,', 'comforting notes and a smooth,', 'mellow aroma.'];
    body.forEach((l, i) => P.push(T('sans', l, 2.25, 6, 47 + i * 3.4, c.frameInk, { opacity: 0.9 })));
    P.push(rule(6, 72.5, w - 5, c.frameInk, 0.2));
    const note = ['The vanilla on this box is a 19th-century watercolour of Vanilla planifolia,', 'painted in Ceylon by George De Alwis.'];
    note.forEach((l, i) => P.push(T('sans', l, 1.85, 6, 76.4 + i * 2.8, c.frameSub)));
    return P.join('');
  };

  VS.frontPlate = frontPlate;
  VS.backPlate = backPlate;

  // ---------------------------------------------------------------------------
  // Assembly

  const sizeOf = (key) => { const p = VS.PANELS[key].panel; return { w: VS.mm(p.w), h: VS.mm(p.h) }; };

  // One face as a standalone SVG (used for 3D textures and previews).
  const panelFn = (key, c) => (c.design === 'plate' && (key === 'front' || key === 'back')) ? VS[key + 'Plate'] : VS[key];
  const getC = (cw) => Object.assign({ id: typeof cw === 'string' ? cw : 'custom' }, VS.COLORWAYS[cw] || cw);

  VS.faceSVG = (key, cw) => {
    const c = getC(cw);
    const { w, h } = sizeOf(key);
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${n(w)}mm" height="${n(h)}mm" viewBox="0 0 ${n(w)} ${n(h)}">` +
      `<defs><clipPath id="f"><rect width="${n(w)}" height="${n(h)}"/></clipPath></defs>` +
      `<g clip-path="url(#f)">${panelFn(key, c)(c, w, h)}</g></svg>`;
  };

  // The whole print sheet on the source artboard, with the verbatim dieline on top.
  VS.sheetSVG = (cw, o = {}) => {
    const c = getC(cw);
    const A = VS.ARTBOARD;
    let defs = '', art = '';
    Object.entries(VS.PANELS).forEach(([key, { panel, region }]) => {
      const { w, h } = sizeOf(key);
      defs += `<clipPath id="clip-${key}"><rect x="${region.x}" y="${region.y}" width="${n(region.w)}" height="${n(region.h)}"/></clipPath>`;
      art += `<g id="${key}" clip-path="url(#clip-${key})"><g transform="translate(${panel.x} ${panel.y}) scale(${n(MM, 6)})">${panelFn(key, c)(c, w, h)}</g></g>`;
    });
    const die = o.dieline === false ? '' : `<g id="Dieline">${root.VS_DIELINE || ''}</g>`;
    const bg = o.paper ? `<rect width="${A.w}" height="${A.h}" fill="${o.paper}"/>` : '';
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${A.w}pt" height="${A.h}pt" viewBox="0 0 ${A.w} ${A.h}">` +
      `<title>Natural Vanilla Tea – ${c.name}</title><defs>${defs}</defs>${bg}<g id="Artwork">${art}</g>${die}</svg>`;
  };

  root.VS = VS;
})(typeof window !== 'undefined' ? window : globalThis);
