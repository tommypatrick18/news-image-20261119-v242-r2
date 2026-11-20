// render.js — news-image-20261119 v242-R2 ("The World in One Day").
// Draws page.html twice in headless Chromium and demands identical bytes.
// Audit first (same context), then two screenshots, then a saved copy.
// Deterministic by construction: fixed viewport, pinned local fonts,
// no network, no clock, no randomness anywhere in the page or here.
//
// Usage: node render.js
// Writes: build/audit.json, build/raw-run1.png, build/raw-run2.png,
//         build/raw-1024.png (run 1, once both runs agree).
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const HERE = __dirname;
const CHROME_BIN = path.join(process.env.HOME, '.cache/ms-playwright/chromium-1255/chrome-linux64/chrome');
const PAGE_URL = 'file://' + path.join(HERE, 'page.html');
const OUTDIR = path.join(HERE, 'build');

const hashFile = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const runChrome = (flags) => execFileSync(CHROME_BIN, flags, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });

fs.mkdirSync(OUTDIR, { recursive: true });

const baseFlags = [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  '--hide-scrollbars', '--force-device-scale-factor=1',
  '--window-size=1024,1024', '--virtual-time-budget=10000',
];

// Step 1: overflow audit from the same Chromium context.
const dumped = runChrome([...baseFlags, '--dump-dom', PAGE_URL]);
const found = dumped.match(/<pre id="audit">([\s\S]*?)<\/pre>/);
if (!found) { console.error('audit block missing from dumped DOM'); process.exit(1); }
const audit = JSON.parse(found[1].replace(/&quot;/g, '"').replace(/&amp;/g, '&'));
fs.writeFileSync(path.join(OUTDIR, 'audit.json'), JSON.stringify(audit, null, 2) + '\n');
const badTexts = audit.texts.filter((e) => e.over);
const badBands = audit.bands.filter((b) => b.over);
console.log(`audit: ${audit.texts.length} text nodes, ${badTexts.length} overflowing, bands overflowing: ${badBands.length}, fonts: ${audit.fontsReady}`);
badTexts.forEach((e) => console.log(`  OVERFLOW ${e.id} dw=${e.dw} dh=${e.dh} "${e.text}"`));
badBands.forEach((b) => console.log(`  BAND OVERFLOW ${b.band}`));

// Step 2: two independent screenshot runs; bytes must agree.
const first = path.join(OUTDIR, 'raw-run1.png');
const second = path.join(OUTDIR, 'raw-run2.png');
runChrome([...baseFlags, '--screenshot=' + first, PAGE_URL]);
runChrome([...baseFlags, '--screenshot=' + second, PAGE_URL]);
const digest1 = hashFile(first), digest2 = hashFile(second);
console.log(`run1: ${fs.statSync(first).size} bytes sha256 ${digest1}`);
console.log(`run2: ${fs.statSync(second).size} bytes sha256 ${digest2}`);
if (digest1 !== digest2) { console.error('DETERMINISM FAIL: the two renders differ'); process.exit(1); }
fs.copyFileSync(first, path.join(OUTDIR, 'raw-1024.png'));
console.log('determinism: OK (both renders byte-identical)');
console.log('chrome: ' + runChrome(['--version']).trim());
