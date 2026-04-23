const { test, expect } = require("@playwright/test");

test.describe("Nous Research keyword site", () => {
  test("desktop homepage renders SEO content, sources, and assets", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/Nous Research/i);
    await expect(page.locator("h1")).toHaveText("Nous Research");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /Independent guide to Nous Research/i);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://nousresearch.lol/");
    await expect(page.getByText("Independent resource.")).toBeVisible();

    await expect(page.getByRole("link", { name: "Official Site" }).first()).toHaveAttribute("href", "https://nousresearch.com/");
    await expect(page.getByRole("link", { name: "View GitHub" })).toHaveAttribute("href", "https://github.com/nousresearch");
    await expect(page.getByRole("link", { name: /Hermes 4/i })).toHaveAttribute("href", "https://hermes4.nousresearch.com/");
    await expect(page.getByRole("link", { name: /Hugging Face/i })).toHaveAttribute("href", "https://huggingface.co/NousResearch");

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("mobile layout stays inside the viewport and keeps main sections reachable", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");
    await expect(page.locator("h1")).toBeVisible();
    await page.getByRole("link", { name: "Explore Research Areas" }).click();
    await expect(page.locator("#overview")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);
    await expect(page.getByRole("heading", { name: "Quick answers for the Nous Research keyword." })).toBeVisible();

    await context.close();
  });

  test("static metadata files are served", async ({ page }) => {
    const favicon = await page.request.get("/assets/brand/favicon.png");
    expect(favicon.ok()).toBe(true);
    expect(favicon.headers()["content-type"]).toContain("image/png");

    const manifest = await page.request.get("/site.webmanifest");
    expect(manifest.ok()).toBe(true);
    expect(manifest.headers()["content-type"]).toContain("application/manifest+json");

    const sitemap = await page.request.get("/sitemap.xml");
    expect(sitemap.ok()).toBe(true);
    expect(await sitemap.text()).toContain("https://nousresearch.lol/");
  });
});
