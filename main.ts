// Entry point for the make.fun grader.
//
// Copies the judged image (entry.png, sitting beside this file) into the
// directory named by the MAKEFUN_OUTPUT_DIR environment variable
// (default: /output). Node standard library only; runs offline.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), dest);
console.log(`copied entry.png -> ${dest}`);
