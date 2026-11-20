// news-image-20261119: a one-page newspaper front page summing up
// Thursday 19 November 2026, drawn offline by draw.py and committed
// beside this file as entry.png. This program copies that image to
// the output directory (MAKEFUN_OUTPUT_DIR, or /output in the grader).
// Node 22, standard library only; no network, deterministic bytes.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error(`entry.png not found beside main.ts (${src})`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`wrote ${dst} (${statSync(dst).size} bytes)`);
