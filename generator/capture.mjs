// Screenshots of the live sites. Needs playwright; run from the repo root.
import { chromium } from "playwright";
import { readFileSync, mkdirSync } from "node:fs";

const { live } = JSON.parse(readFileSync("data/content.json", "utf8"));
mkdirSync("assets/raw", { recursive: true });
const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist", "--enable-unsafe-swiftshader"] });

for (const site of live) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(site.url, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: `assets/raw/${site.id}.jpg`, type: "jpeg", quality: 82 });
  await page.close();
}
await browser.close();
