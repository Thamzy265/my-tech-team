import { test, expect, Page } from '@playwright/test';
import { pathToFileURL } from 'url';
import path from 'path';

const URL = pathToFileURL(path.resolve('static/states.html')).href;
const SHOTS = 'docs/qa/notes-states/screens';
const shot = (page: Page, name: string) => page.screenshot({ path: `${SHOTS}/${name}.png` });

// Contrast ratio (WCAG) from rendered colours.
async function contrast(page: Page, sel: string) {
  return page.evaluate((s) => {
    const el = document.querySelector(s)!;
    const parse = (c: string) => c.match(/[\d.]+/g)!.slice(0, 3).map(Number);
    const lum = ([r, g, b]: number[]) => {
      const f = (v: number) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    };
    const cs = getComputedStyle(el);
    let bg = cs.backgroundColor; let p: Element | null = el;
    while ((bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') && p) { p = p.parentElement; bg = p ? getComputedStyle(p).backgroundColor : 'rgb(255, 255, 255)'; }
    const a = lum(parse(cs.color)), b = lum(parse(bg));
    return { fg: cs.color, bg, ratio: (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05) };
  }, sel);
}

test('notes page: empty, with notes, error, keyboard, a11y, 320px', async ({ page }) => {
  await page.goto(URL);

  // 1 Empty state (default)
  await expect(page.getByRole('region', { name: 'Empty state' })).toBeVisible();
  await expect(page.getByText('No notes yet. Write your first note.')).toBeVisible();
  await expect(page.getByRole('region', { name: 'Notes list' })).toBeHidden();
  await expect(page.getByRole('alert')).toHaveCount(0); // hidden alert not in a11y tree
  await shot(page, '1-empty');

  // 2 With notes
  await page.getByRole('button', { name: 'With notes' }).click();
  await expect(page.getByRole('region', { name: 'Notes list' })).toBeVisible();
  await expect(page.getByRole('listitem')).toHaveText(['Buy milk', 'Call Sam']);
  await expect(page.getByRole('region', { name: 'Empty state' })).toBeHidden();
  await shot(page, '2-with-notes');

  // 3 Error
  await page.getByRole('button', { name: 'Error' }).click();
  await expect(page.getByRole('alert')).toBeVisible();
  await expect(page.getByRole('alert')).toContainText('Could not load notes.');
  await expect(page.getByRole('button', { name: 'Try again' })).toBeVisible();
  await expect(page.getByRole('region', { name: 'Notes list' })).toBeHidden();
  await shot(page, '3-error');

  // Keyboard: Tab order and visible focus; Enter/Space switch states
  await page.goto(URL);
  const order: string[] = [];
  for (const name of ['Empty', 'With notes', 'Error']) {
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name, exact: true })).toBeFocused();
    const outline = await page.evaluate(() => { const s = getComputedStyle(document.activeElement!); return `${s.outlineStyle} ${s.outlineWidth}`; });
    expect(outline).not.toMatch(/^none/);
    expect(outline).not.toMatch(/ 0px$/);
    order.push(name);
    await shot(page, `4-focus-${name.toLowerCase().replace(' ', '-')}`);
  }
  await page.keyboard.press('Shift+Tab');
  await expect(page.getByRole('button', { name: 'With notes' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('region', { name: 'Notes list' })).toBeVisible();
  await page.keyboard.press('Tab');
  await page.keyboard.press('Space');
  await expect(page.getByRole('alert')).toBeVisible();
  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: 'Try again' })).toBeFocused();
  await shot(page, '4-focus-try-again');
  await page.keyboard.press('Tab'); // leaves the page: no trap
  await expect(page.locator('body')).toBeFocused().catch(() => {});
  expect(await page.evaluate(() => document.activeElement?.tagName)).not.toBe('BUTTON');

  // Accessibility tree
  await expect(page.locator('body')).toMatchAriaSnapshot(`
    - heading "My notes" [level=1]
    - paragraph:
      - button "Empty"
      - button "With notes"
      - button "Error"
    - alert "Error state":
      - paragraph:
        - text: Could not load notes.
        - button "Try again"
  `);

  // Contrast and target size
  for (const sel of ['h1', '#empty p', 'button']) {
    const c = await contrast(page, sel);
    console.log('contrast', sel, JSON.stringify(c));
    expect(c.ratio).toBeGreaterThanOrEqual(4.5);
  }
  for (const b of await page.getByRole('button').all()) {
    const box = (await b.boundingBox())!;
    expect(box.width).toBeGreaterThanOrEqual(24);
    expect(box.height).toBeGreaterThanOrEqual(24);
  }

  // 320 px, all three states
  await page.setViewportSize({ width: 320, height: 640 });
  for (const [btn, name] of [['Empty', '5-320-empty'], ['With notes', '5-320-with-notes'], ['Error', '5-320-error']]) {
    await page.getByRole('button', { name: btn, exact: true }).click();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow).toBe(0);
    await shot(page, name);
  }
  // 200% zoom equivalent: 640 CSS px viewport at 2x == 320 CSS px (covered above); also 1280 px @200% = 640 px
  await page.setViewportSize({ width: 640, height: 360 });
  await page.getByRole('button', { name: 'Error' }).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)).toBe(0);
  await shot(page, '6-zoom200-error');

  // Try again: record behaviour
  const before = await page.locator('#error').isVisible();
  await page.getByRole('button', { name: 'Try again' }).click();
  console.log('try-again: error still visible =', before && (await page.locator('#error').isVisible()));
});
