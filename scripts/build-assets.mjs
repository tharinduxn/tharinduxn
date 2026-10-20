#!/usr/bin/env node
/**
 * Generates the two animated SVGs used by README.md
 *
 *   assets/portrait.svg  <- wraps assets/binary-portrait.png in a lens with animated rings
 *   assets/typing.svg    <- terminal-style chip that types out your roles
 *
 * Usage:  node scripts/build-assets.mjs
 * No dependencies. If `sharp` happens to be installed, the photo is downsized first.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

/* ───────────────────────── Edit these ───────────────────────── */
const CONFIG = {
  photo: 'binary-portrait.png',          // lives in /assets
  pill: 'online',                        // small status pill under the portrait
  prefix: 'I build',                     // static text in the typing chip
  phrases: [
    'responsive React & Next.js apps',
    'polished Flutter mobile apps',
    'design systems with clean architecture',
  ],
  color: {
    tail: '#4F7CFF',                     // comet tail
    mid: '#38B6F5',
    head: '#22C7F0',                     // comet head + glow
    lens: '#0D1117',                     // disc behind the portrait (shows through transparent PNGs)
    chip: '#0D1117',
    chipStroke: '#30363D',
    text: '#E6EDF3',
    dim: '#8B949E',
    live: '#3FB950',
  },
  maxPhotoPx: 640,                       // photo is downsized to this if `sharp` is available
};
/* ─────────────────────────────────────────────────────────────── */

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const assets = resolve(root, 'assets');
mkdirSync(assets, { recursive: true });
const c = CONFIG.color;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const f = (n) => +n.toFixed(3);

/* ───────────────────────── typing.svg ───────────────────────── */
function buildTyping() {
  const FONT = "ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace";
  const SIZE = 15, CW = 9;                       // font size and fixed character cell (px)
  const H = 40, PAD = 16, PROMPT_W = 18;
  const prefix = CONFIG.prefix.trim();            // trailing spaces get trimmed by XML, so add the gap in px
  const textX = PAD + PROMPT_W + (prefix.length + 1) * CW;
  const longest = Math.max(...CONFIG.phrases.map((p) => p.length));
  const W = Math.ceil(textX + longest * CW + 8 + PAD);

  const WINDOW = 6.2;                            // seconds per phrase
  const D = WINDOW * CONFIG.phrases.length;      // full loop
  const pct = (t) => f((t / D) * 100) + '%';

  let css = '', groups = '', caretFrames = [];
  CONFIG.phrases.forEach((phrase, i) => {
    const n = phrase.length;
    const s = i * WINDOW;
    const typeT = n * 0.055, eraseT = n * 0.025;
    const hold = WINDOW - typeT - eraseT - 0.6;
    const tA = s, tB = s + typeT, tC = tB + hold, tD = tC + eraseT;
    const reveal = n * CW;

    css += `
@keyframes cover${i}{
  0%{transform:translateX(0)}
  ${pct(tA)}{transform:translateX(0);animation-timing-function:steps(${n})}
  ${pct(tB)}{transform:translateX(${reveal}px)}
  ${pct(tC)}{transform:translateX(${reveal}px);animation-timing-function:steps(${n})}
  ${pct(tD)}{transform:translateX(0)}
  100%{transform:translateX(0)}
}
@keyframes show${i}{
  0%{opacity:0}
  ${pct(Math.max(tA - 0.001, 0))}{opacity:0}
  ${pct(tA)}{opacity:1}
  ${pct(tD)}{opacity:1}
  ${pct(tD + 0.001)}{opacity:0}
  100%{opacity:0}
}
.g${i}{animation:show${i} ${D}s steps(1,end) infinite}
.c${i}{animation:cover${i} ${D}s linear infinite}`;

    caretFrames.push(
      `${pct(tA)}{transform:translateX(0);animation-timing-function:steps(${n})}`,
      `${pct(tB)}{transform:translateX(${reveal}px)}`,
      `${pct(tC)}{transform:translateX(${reveal}px);animation-timing-function:steps(${n})}`,
      `${pct(tD)}{transform:translateX(0)}`,
    );

    groups += `
  <g class="g${i}">
    <text x="${textX}" y="25" textLength="${reveal}" lengthAdjust="spacing" fill="${c.text}">${esc(phrase)}</text>
    <rect class="c${i}" x="${textX}" y="10" width="${W - textX - PAD + 6}" height="20" fill="${c.chip}"/>
  </g>`;
  });

  const label = CONFIG.prefix + ' ' + CONFIG.phrases.join(', ');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(label)}">
  <title>${esc(label)}</title>
  <style>
    text{font-family:${FONT};font-size:${SIZE}px}
    .caret{animation:caretMove ${D}s linear infinite,blink 1.1s steps(1,end) infinite}
    @keyframes caretMove{0%{transform:translateX(0)}${caretFrames.join('')}100%{transform:translateX(0)}}
    @keyframes blink{0%,55%{opacity:1}56%,100%{opacity:0}}${css}
    @media (prefers-reduced-motion:reduce){
      .caret{animation:none;opacity:0}
      .g1,.g2,.g3,.g4,.g5{animation:none;opacity:0}
      .g0{animation:none;opacity:1}
      .c0{animation:none;transform:translateX(${CONFIG.phrases[0].length * CW}px)}
    }
  </style>
  <rect x=".5" y=".5" width="${W - 1}" height="${H - 1}" rx="10" fill="${c.chip}"/>
  <text x="${PAD}" y="25" fill="${c.head}">›</text>
  <text x="${PAD + PROMPT_W}" y="25" textLength="${prefix.length * CW}" lengthAdjust="spacing" fill="${c.dim}">${esc(prefix)}</text>${groups}
  <rect class="caret" x="${textX}" y="11" width="${CW - 1}" height="18" rx="1" fill="${c.head}"/>
  <rect x=".5" y=".5" width="${W - 1}" height="${H - 1}" rx="10" fill="none" stroke="${c.chipStroke}"/>
</svg>
`;
}

/* ───────────────────────── portrait.svg ───────────────────────── */
async function buildPortrait() {
  const photoPath = resolve(assets, CONFIG.photo);
  if (!existsSync(photoPath)) {
    console.warn(`! Skipped portrait.svg — put your picture at assets/${CONFIG.photo} and re-run.`);
    return null;
  }
  let buf = readFileSync(photoPath);
  let mime = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp' }[extname(photoPath).toLowerCase()] || 'image/png';
  try {
    const { default: sharp } = await import('sharp');
    const img = sharp(buf).resize({ width: CONFIG.maxPhotoPx, height: CONFIG.maxPhotoPx, fit: 'inside', withoutEnlargement: true });
    buf = await (mime === 'image/png' ? img.png({ compressionLevel: 9 }) : img).toBuffer();
  } catch { /* sharp not installed — use the file as is */ }
  const b64 = buf.toString('base64');
  if (b64.length > 3_500_000) {
    console.warn(`! Photo is ${(b64.length / 1e6).toFixed(1)} MB once embedded. GitHub may refuse to load it — resize it to ~640px wide first.`);
  }

  const W = 320, H = 332, cx = 160, cy = 160, R = 118;       // lens radius
  const FONT = "ui-monospace, 'JetBrains Mono', SFMono-Regular, Menlo, Consolas, monospace";
  const pt = (r, deg) => [f(cx + r * Math.cos((deg * Math.PI) / 180)), f(cy + r * Math.sin((deg * Math.PI) / 180))];
  const arc = (r, from, to, color, op, w, extra = '') => {
    const [x0, y0] = pt(r, from), [x1, y1] = pt(r, to);
    const large = to - from > 180 ? 1 : 0;
    return `<path d="M${x0} ${y0}A${r} ${r} 0 ${large} 1 ${x1} ${y1}" fill="none" stroke="${color}" stroke-opacity="${op}" stroke-width="${w}" stroke-linecap="round" ${extra}/>`;
  };
  const textW = CONFIG.pill.length * 7.4;
  const pillW = Math.round(14 + 7 + 8 + textW + 14);
  const dotX = -pillW / 2 + 14 + 3.5;
  const textX = dotX + 3.5 + 8;
  const headAngle = 300;
  const [hx, hy] = pt(136, headAngle);

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Animated binary portrait of Tharindu Nimesh">
  <title>Tharindu Nimesh — binary portrait</title>
  <defs>
    <clipPath id="lens"><circle cx="${cx}" cy="${cy}" r="${R}"/></clipPath>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <style>
    .rot{transform-box:view-box;transform-origin:${cx}px ${cy}px}
    .spin{animation:spin 9s linear infinite}
    .spin-slow{animation:spin 48s linear infinite reverse}
    .breathe{animation:breathe 3.6s ease-in-out infinite}
    .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}
    text{font-family:${FONT};font-size:12px;letter-spacing:.4px}
    @keyframes spin{to{transform:rotate(360deg)}}
    @keyframes breathe{0%,100%{stroke-opacity:.14}50%{stroke-opacity:.5}}
    @keyframes pulse{0%{transform:scale(1);opacity:.7}100%{transform:scale(2.8);opacity:0}}
    @media (prefers-reduced-motion:reduce){
      .spin,.spin-slow,.breathe,.pulse{animation:none}
      .pulse{opacity:0}
    }
  </style>

  <!-- outer dashed ring, slow counter-rotation -->
  <g class="rot spin-slow"><circle cx="${cx}" cy="${cy}" r="148" fill="none" stroke="${c.mid}" stroke-opacity=".32" stroke-width="1" stroke-dasharray="1.5 7"/></g>

  <!-- comet ring -->
  <circle cx="${cx}" cy="${cy}" r="136" fill="none" stroke="${c.tail}" stroke-opacity=".12" stroke-width="1"/>
  <g class="rot spin">
    ${arc(136, headAngle - 210, headAngle, c.tail, 0.35, 2)}
    ${arc(136, headAngle - 120, headAngle, c.mid, 0.7, 2.5)}
    <g filter="url(#glow)">
      ${arc(136, headAngle - 42, headAngle, c.head, 1, 3)}
      <circle cx="${hx}" cy="${hy}" r="4" fill="#fff"/>
      <circle cx="${hx}" cy="${hy}" r="4" fill="${c.head}" fill-opacity=".55"/>
    </g>
  </g>

  <!-- lens: backdrop, photo, edge -->
  <circle cx="${cx}" cy="${cy}" r="${R}" fill="${c.lens}"/>
  <image xlink:href="data:${mime};base64,${b64}" x="${cx - R}" y="${cy - R}" width="${2 * R}" height="${2 * R}" preserveAspectRatio="xMidYMid slice" clip-path="url(#lens)"/>
  <circle class="breathe" cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${c.head}" stroke-width="1.25"/>

  <!-- status pill -->
  <g transform="translate(${cx} 305)">
    <rect x="${-pillW / 2}" y="-13" width="${pillW}" height="26" rx="13" fill="${c.chip}" stroke="${c.chipStroke}"/>
    <circle class="pulse" cx="${dotX}" cy="0" r="3.5" fill="${c.live}"/>
    <circle cx="${dotX}" cy="0" r="3.5" fill="${c.live}"/>
    <text x="${textX}" y="4" fill="${c.text}">${esc(CONFIG.pill)}</text>
  </g>
</svg>
`;
}

/* ───────────────────────── run ───────────────────────── */
writeFileSync(resolve(assets, 'typing.svg'), buildTyping());
console.log('✓ assets/typing.svg');
const portrait = await buildPortrait();
if (portrait) {
  writeFileSync(resolve(assets, 'portrait.svg'), portrait);
  console.log('✓ assets/portrait.svg');
}
