# Loqin Website SEO Implementation Plan

## Objective

Improve Loqin's organic discovery and qualified installer downloads by making the site easy to crawl, clear about its Windows and macOS support, useful for VIT Wi-Fi search intent, and measurable in search tools. Preserve the site's visual identity and existing download/release flow.

This file is an implementation brief. The source for the website lives in this repository (`main.py`, `templates/index.html`, and `public/`), not in the Loqin desktop-app repository.

## Current audit notes

Live pages were reviewed on 2026-11-12 at `https://loqin.aayushsrivastava.com/`:

- The homepage returns HTML with a title, meta description, one H1, and readable page content.
- The homepage title is `Loqin PC - Automated VIT Hostel Wi-Fi Client`; its description currently calls Loqin a Windows tray app, though the site also offers a macOS installer.
- Several feature paragraphs describe Windows-only capabilities, which makes platform support unclear.
- The homepage head did not include a canonical URL, Open Graph/Twitter metadata, or JSON-LD structured data.
- `/robots.txt` and `/sitemap.xml` returned 404 pages during the live check.
- Privacy and license pages return HTML and have their own titles and descriptions.
- Firecrawl could not parse `/download` and reported a large file response. Inspect the route and response headers before changing it; it may intentionally serve an installer rather than an HTML page.

These observations are a point-in-time audit, not a claim about search rankings or traffic. Re-check current source and live behavior before implementation.

## Phase 1: Establish the site's canonical identity and crawl paths

1. Confirm `https://loqin.aayushsrivastava.com/` is the preferred public origin. Redirect alternate hosts and HTTP to HTTPS and the preferred host with a single permanent redirect where hosting supports it.
2. Add a real `/robots.txt` response. Allow public pages to be crawled and include the absolute sitemap URL. Do not block CSS, JavaScript, images, or other resources needed to render the site.
3. Add a valid `/sitemap.xml` containing only canonical, public HTML URLs that return `200`: homepage, useful platform/setup/help pages added below, and privacy/license pages if they should be indexed. Exclude installer binaries, duplicate query-string variants, redirects, and error pages. Keep `lastmod` accurate if emitted.
4. Ensure the custom not-found route returns HTTP `404`, not a `200` soft-404. Check that redirects and unknown paths do not create duplicate indexable pages.
5. Keep download URLs functional. If `/download` is a direct installer endpoint, create or retain a separate crawlable HTML download landing page and make buttons link from that page to the correct installer/release. Do not put binary downloads in the XML sitemap.

## Phase 2: Improve page metadata and social previews

1. Give every indexable page a unique, accurate `<title>` and meta description. Avoid keyword stuffing and avoid identical metadata on all pages.
2. Add a self-referencing canonical URL to each indexable HTML page, using the custom domain and a normalized trailing-slash policy. Ensure query parameters used to choose an OS do not create duplicate canonical pages.
3. Add Open Graph metadata (`og:title`, `og:description`, `og:type`, `og:url`, `og:image`) and Twitter card metadata. Use an accessible, branded preview image with an absolute HTTPS URL and suitable dimensions.
4. Add JSON-LD `SoftwareApplication` structured data to the home or download page. Include only verified information such as name, application category, operating systems, website, source/release links, and offer details. Do not claim ratings, pricing, VIT endorsement, or other facts the project cannot substantiate.
5. Preserve semantic heading order: one descriptive H1 per page, followed by useful H2/H3 sections. Keep primary copy server-rendered in the HTML rather than dependent on client-side script execution.

Suggested homepage metadata and headline direction (refine to fit final copy):

- Title: `Loqin | VIT Hostel Wi-Fi Auto Login for Windows & macOS`
- Description: `Automatically reconnect to VIT hostel Wi-Fi with Loqin, a lightweight tray app for Windows and macOS. Set up once and let Loqin handle re-authentication.`
- H1: `Automatically log in to VIT hostel Wi-Fi on Windows and macOS`

Only use the macOS claim on pages and feature descriptions where the current macOS app actually supports the described behavior.

## Phase 3: Make the platform story accurate and useful

1. Update the homepage hero, feature copy, download labels, and metadata so they consistently explain that Loqin is available for Windows and macOS, while distinguishing platform-specific behavior.
2. Replace vague feature claims with concise explanations of what the app does, what setup requires, where credentials are stored, and what the user should expect after installation. Keep security and privacy claims consistent with the app and the published privacy policy.
3. Add substantive, indexable pages for high-intent needs, preferably using the site's current server-rendered templates:
   - `/windows` or `/windows-setup`: requirements, installation, setup, supported Windows versions, and screenshots.
   - `/macos` or `/macos-setup`: requirements, permissions, installation, setup, supported macOS versions, and platform-specific limitations.
   - `/troubleshooting`: practical steps for captive portals, failed authentication, network switching, and update problems.
   - `/how-it-works` or a substantial FAQ: explain automatic re-authentication, local credential handling, compatibility, and how to pause or remove the app.
4. Keep pages genuinely distinct and useful. Do not create near-identical campus/location pages or thin keyword landing pages. Do not imply that Loqin is an official VIT product unless that is verifiably true.
5. Add contextual internal links between the homepage, platform setup pages, troubleshooting, privacy policy, source code, and downloads. Use descriptive link text such as `Windows setup guide`, not repeated generic `click here` links.

Treat phrases such as `VIT hostel Wi-Fi auto login`, `VIT Wi-Fi client for Windows`, `VIT Wi-Fi client for macOS`, and `automatic captive portal login` as hypotheses to validate in Search Console. No search-volume or ranking measurements were available in this audit.

## Phase 4: Improve images and page experience

1. Inspect image sizes and formats. Convert oversized raster assets to appropriately sized WebP/AVIF or optimized PNG/JPEG where browser and hosting support allow. Keep a fallback if needed.
2. Add intrinsic `width` and `height` to images to avoid layout shifts. Use descriptive alt text for meaningful screenshots and empty alt text for decorative imagery.
3. Do not lazy-load the primary above-the-fold hero image; lazy-load below-the-fold screenshots and non-critical images.
4. Review font loading and third-party requests. Keep the visual fonts if they are worth the cost, but limit font families/weights, use `font-display: swap`, and avoid blocking page content on external resources.
5. Check mobile layout, keyboard access, contrast, and Core Web Vitals with real measurements. Prioritize the largest contentful paint element, cumulative layout shift, and interaction responsiveness based on field or lab evidence rather than guessing.

## Phase 5: Search measurement and release readiness

1. Confirm the existing Google verification tag belongs to the intended Search Console property. Set up a domain property for the canonical domain if not already present.
2. Submit the sitemap in Google Search Console and Bing Webmaster Tools. Inspect the homepage and new pages with URL inspection after deployment; verify canonical selection, indexing eligibility, and sitemap processing.
3. Configure analytics only if desired and consistent with the privacy policy. Do not add tracking scripts merely to claim SEO measurement.
4. Record a baseline before implementation: indexed URLs, impressions, clicks, query mix, click-through rate, and Core Web Vitals where available. Compare after changes over an appropriate period; do not promise traffic growth or treat a single crawl as proof of indexing.
5. Before publishing, review rendered HTML and response codes for every public route, validate sitemap XML and JSON-LD, check internal/external links, and confirm installer links resolve to the intended current release.

## Acceptance criteria

- The canonical homepage and every intended public page return `200` with unique title/description, a correct canonical, and useful server-rendered content.
- `/robots.txt` and `/sitemap.xml` return valid responses; the sitemap contains only canonical indexable pages.
- The site accurately distinguishes Windows and macOS support and does not make unsupported security, compatibility, or affiliation claims.
- Structured data and social metadata validate and match visible page content.
- Search-intent pages answer real setup/troubleshooting questions and are linked from relevant pages.
- Installer routes remain correct, and the download landing page is readable and useful without interfering with direct downloads.
- Mobile and performance checks are measured and recorded; no fabricated SEO score or traffic forecast is included.
- Changes are verified locally and in preview. Do not publish/deploy the site as part of this implementation unless separately authorized.
