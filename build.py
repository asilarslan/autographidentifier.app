#!/usr/bin/env python3
"""Static site generator for autographidentifier.app.

    python3 build.py            # rebuild pages from src/ using cached ratings
    python3 build.py --refresh  # also re-fetch the App Store rating first

Content lives in src/people.py (signature guides) and src/articles.py (blog).
Generated files are committed, because GitHub Pages serves the repo as-is.
"""
import html
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from articles import ARTICLES  # noqa: E402
from people import PEOPLE  # noqa: E402

SITE = "https://autographidentifier.app"
APP_ID = "6749822952"
APP_STORE = f"https://apps.apple.com/app/autograph-identifier/id{APP_ID}"
PLAY_STORE = "https://play.google.com/store/apps/details?id=com.autographidentifier"
EMAIL = "asilarslan93@gmail.com"
YEAR = date.today().year
TODAY = date.today().isoformat()
RATINGS_FILE = ROOT / "src" / "ratings.json"

e = html.escape


def load_ratings(refresh):
    if refresh:
        url = f"https://itunes.apple.com/lookup?id={APP_ID}&country=us"
        with urllib.request.urlopen(url, timeout=20) as r:
            app = json.load(r)["results"][0]
        data = {
            "value": round(app["averageUserRating"], 1),
            "count": app["userRatingCount"],
            "fetched": TODAY,
        }
        RATINGS_FILE.write_text(json.dumps(data, indent=2) + "\n")
    return json.loads(RATINGS_FILE.read_text())


RATING = load_ratings("--refresh" in sys.argv)


def stars(value):
    full = int(round(value))
    return "★" * full + "☆" * (5 - full)


def badges():
    return f"""<div class="badges">
    <a href="{APP_STORE}" aria-label="Download Autograph Identifier on the App Store"><img class="badge-apple" src="/assets/app-store-badge.svg" alt="Download on the App Store" width="162" height="54"></a>
    <a href="{PLAY_STORE}" aria-label="Get Autograph Identifier on Google Play"><img class="badge-google" src="/assets/google-play-badge.png" alt="Get it on Google Play" width="207" height="80"></a>
</div>"""


def rating_pill():
    return (f'<div class="rating"><span class="stars" aria-hidden="true">{stars(RATING["value"])}</span> '
            f'{RATING["value"]} on the App Store · {RATING["count"]} ratings</div>')


def json_ld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def crumb_schema(trail):
    return json_ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + path}
            for i, (name, path) in enumerate(trail)
        ],
    })


def faq_html(faq):
    items = "\n".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)
    return f'<div class="faq">{items}</div>'


def layout(path, title, desc, body, schema="", og_type="website"):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <link rel="canonical" href="{url}">
    <meta name="apple-itunes-app" content="app-id={APP_ID}">
    <meta name="theme-color" content="#2563eb">

    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="Autograph Identifier">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(desc)}">
    <meta property="og:image" content="{SITE}/assets/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{e(title)}">
    <meta name="twitter:description" content="{e(desc)}">
    <meta name="twitter:image" content="{SITE}/assets/og-image.png">

    <link rel="icon" type="image/png" href="/assets/logo-96.png">
    <link rel="apple-touch-icon" href="/assets/logo-192.png">
    <link rel="manifest" href="/manifest.json">
    <link rel="stylesheet" href="/assets/style.css">
    {schema}
</head>
<body>
    <header class="site">
        <nav class="container">
            <a class="logo" href="/"><img src="/assets/logo-96.png" alt="" width="34" height="34">Autograph Identifier</a>
            <button class="hamburger" aria-label="Menu" aria-controls="navLinks" aria-expanded="false"><span></span><span></span><span></span></button>
            <ul class="nav-links" id="navLinks">
                <li><a href="/#how-it-works">How It Works</a></li>
                <li><a href="/signatures/">Signature Guides</a></li>
                <li><a href="/blog/">Blog</a></li>
                <li><a href="/#pricing">Pricing</a></li>
                <li><a class="nav-cta" href="/#download">Get the App</a></li>
            </ul>
        </nav>
    </header>

    <main>
{body}
    </main>

    <footer class="site">
        <div class="container">
            <div class="footer-grid">
                <div>
                    <h4>Autograph Identifier</h4>
                    <p>AI autograph identification and a first-opinion authenticity check, on iPhone, iPad and Android.</p>
                </div>
                <div>
                    <h4>Get the app</h4>
                    <ul>
                        <li><a href="{APP_STORE}">App Store</a></li>
                        <li><a href="{PLAY_STORE}">Google Play</a></li>
                    </ul>
                </div>
                <div>
                    <h4>Learn</h4>
                    <ul>
                        <li><a href="/signatures/">Signature guides</a></li>
                        <li><a href="/blog/">Blog</a></li>
                        <li><a href="/blog/how-to-spot-a-fake-autograph/">Spot a fake autograph</a></li>
                    </ul>
                </div>
                <div>
                    <h4>Support</h4>
                    <ul>
                        <li><a href="mailto:{EMAIL}">Contact</a></li>
                        <li><a href="/terms-of-use.html">Terms of Use</a></li>
                        <li><a href="/privacy-policy.html">Privacy Policy</a></li>
                    </ul>
                </div>
            </div>
            <p class="copy">&copy; {YEAR} Autograph Identifier by Asil Arslan. All rights reserved. Autograph Identifier provides an AI-generated opinion, not a certificate of authenticity, and is not affiliated with any person named on this site or with PSA, JSA, Beckett or Upper Deck.</p>
        </div>
    </footer>

    <script>
        (function () {{
            var btn = document.querySelector('.hamburger');
            var nav = document.getElementById('navLinks');
            function setOpen(open) {{
                nav.classList.toggle('active', open);
                btn.setAttribute('aria-expanded', open ? 'true' : 'false');
            }}
            btn.addEventListener('click', function (ev) {{
                ev.stopPropagation();
                setOpen(!nav.classList.contains('active'));
            }});
            document.addEventListener('click', function (ev) {{
                if (!nav.contains(ev.target) || ev.target.tagName === 'A') setOpen(false);
            }});
        }})();
    </script>
</body>
</html>
"""


def write(path, content):
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def person_card(p):
    return f"""<a class="card" href="/signatures/{p['slug']}/">
    <span class="tag">{e(p['category'])}</span>
    <h3>{e(p['name'])} autograph</h3>
    <p>{e(p['blurb'])}</p>
    <span class="more">Read the guide →</span>
</a>"""


def article_card(a):
    return f"""<a class="card" href="/blog/{a['slug']}/">
    <h3>{e(a['title'])}</h3>
    <p>{e(a['summary'])}</p>
    <span class="more">Read article →</span>
</a>"""


def cta_box(heading, text):
    return f"""<div class="cta-box">
    <h2>{e(heading)}</h2>
    <p>{e(text)}</p>
    {badges()}
    <p class="free-note">Free to download · 1 free scan included</p>
</div>"""


# ---------------------------------------------------------------- home

HOME_FAQ = [
    ("Is Autograph Identifier free?",
     "The app is free to download and includes 1 free scan so you can see a full result before paying anything. "
     "Premium unlocks unlimited scans for $9.99 per week or $49.99 per year."),
    ("What does a scan tell me?",
     "Each result gives the name the signature appears to belong to, an overall assessment such as Likely Authentic "
     "or Unclear, the signature characteristics the AI noticed, any red flags and a confidence level."),
    ("Is the result a certificate of authenticity?",
     "No. It is an AI-generated first opinion that helps you sort items and decide what deserves a closer look. "
     "For valuable pieces you should still use a professional authenticator such as PSA/DNA, JSA or Beckett."),
    ("What can I scan?",
     "Signed photos, baseballs, jerseys, cards, album covers, books and documents. A sharp, well-lit, close photo of "
     "the signature gives the best result. Clear, well-known signatures are identified most reliably; faint or "
     "heavily stylised ones may come back as Unclear."),
    ("Which devices are supported?",
     "iPhone and iPad running iOS 17.5 or later, and Android phones and tablets through Google Play."),
    ("How do I cancel Premium?",
     "Subscriptions are managed by Apple or Google. Cancel any time from your App Store or Google Play subscription "
     "settings and you keep access until the end of the paid period."),
]


def build_home():
    people_cards = "\n".join(person_card(p) for p in PEOPLE)
    article_cards = "\n".join(article_card(a) for a in ARTICLES)
    body = f"""
<section class="hero">
    <div class="container hero-grid">
        <div class="hero-copy">
            {rating_pill()}
            <h1>Who signed it? Is it real? Ask AI in seconds.</h1>
            <p class="lead">Take a photo of any autograph. Autograph Identifier names the signer, gives an authenticity assessment and lists the red flags, before you buy, sell or pay for certification.</p>
            {badges()}
            <p class="free-note"><strong>Free to download · 1 free scan.</strong> See a full result before you pay anything.</p>
        </div>
        <div class="phone">
            <img src="/assets/screens/babe-ruth-result.jpg" alt="Autograph Identifier result for a Babe Ruth signed baseball: Likely Authentic, red flags none detected, confidence level high" width="660" height="1434">
        </div>
    </div>
</section>

<section id="results">
    <div class="container result-grid">
        <div class="shot">
            <img src="/assets/screens/marilyn-monroe-result.jpg" alt="App screenshot: signed Marilyn Monroe photo analysed as Likely Authentic with signature characteristics listed" width="660" height="1434" loading="lazy">
        </div>
        <div>
            <h2>What you get from every scan</h2>
            <p style="margin-bottom:22px;color:var(--muted)">These are real screens from the app, not mock-ups. Each analysis is laid out the same way:</p>
            <ul class="result-list">
                <li><strong><span class="pill ok">LIKELY AUTHENTIC</span><span class="pill unclear">UNCLEAR</span></strong><span>A plain verdict at the top, so you know at a glance where the item stands.</span></li>
                <li><strong>Identified name and signature type</strong><span>Who the signature appears to belong to: athlete, musician, actor, band or historical figure.</span></li>
                <li><strong>Signature characteristics</strong><span>Letter formation, slant, flow and pressure, compared with how that person is known to sign.</span></li>
                <li><strong>Red flags</strong><span>Signs of a printed, traced or hesitant signature, and anything that does not fit.</span></li>
                <li><strong>Confidence level</strong><span>How sure the AI is, so you can tell a strong match from a guess.</span></li>
            </ul>
        </div>
    </div>
</section>

<section id="how-it-works" class="alt">
    <div class="container">
        <div class="section-head">
            <h2>How it works</h2>
            <p>Three steps from photo to answer.</p>
        </div>
        <div class="grid grid-3 steps">
            <div class="step"><h3>Photograph the autograph</h3><p>Use the camera or pick a photo from your library. Get close, keep it sharp and avoid glare.</p></div>
            <div class="step"><h3>Ask "Who signed this? Is it real?"</h3><p>The AI reads the signature and the item it is on, and compares it with how known signers write.</p></div>
            <div class="step"><h3>Read the assessment</h3><p>Name, verdict, characteristics, red flags and confidence. Every scan is saved to your history.</p></div>
        </div>
    </div>
</section>

<section>
    <div class="container">
        <div class="section-head">
            <h2>Photos, baseballs, band sets and more</h2>
            <p>Scan single signatures or items signed by a whole group, and keep everything in one history.</p>
        </div>
        <div class="shots">
            <figure><div class="shot"><img src="/assets/screens/babe-ruth-result.jpg" alt="App screenshot: Babe Ruth signed baseball result" width="660" height="1434" loading="lazy"></div><figcaption>Signed baseball: name, red flags and confidence level</figcaption></figure>
            <figure><div class="shot"><img src="/assets/screens/nirvana-result.jpg" alt="App screenshot: Nirvana band-signed photo result" width="660" height="1434" loading="lazy"></div><figcaption>Band-signed photo with several signatures</figcaption></figure>
            <figure><div class="shot"><img src="/assets/screens/scan-history.jpg" alt="App screenshot: scan history list with Likely Authentic and Unclear results" width="660" height="1434" loading="lazy"></div><figcaption>History of every scan, including the unclear ones</figcaption></figure>
        </div>
    </div>
</section>

<section id="signatures" class="alt">
    <div class="container">
        <div class="section-head">
            <h2>Signature guides</h2>
            <p>What the genuine signature looks like, the fakes to watch for and how to verify it, for the most collected names.</p>
        </div>
        <div class="grid grid-3">
{people_cards}
        </div>
        <p class="fineprint"><a href="/signatures/">See all signature guides →</a></p>
    </div>
</section>

<section id="pricing">
    <div class="container narrow">
        <div class="section-head">
            <h2>Try it free, upgrade if it helps</h2>
            <p>You see a complete result before deciding anything.</p>
        </div>
        <div class="grid grid-2">
            <div class="card plan">
                <h3>Free</h3>
                <div class="price">$0</div>
                <ul>
                    <li><strong>1 free scan</strong></li>
                    <li>Signature identification</li>
                    <li>Authenticity assessment</li>
                    <li>Scan history</li>
                </ul>
            </div>
            <div class="card plan featured">
                <h3>Premium</h3>
                <div class="price">$49.99 <small>/ year</small></div>
                <p>or $9.99 / week</p>
                <ul>
                    <li><strong>Unlimited scans</strong></li>
                    <li>Confidence scoring and red flag detection</li>
                    <li>Detailed authenticity breakdown</li>
                    <li>Export and share analysis reports</li>
                    <li>Priority processing and support</li>
                </ul>
            </div>
        </div>
        <p class="fineprint">Prices in USD and may vary by country. Subscriptions renew automatically and can be cancelled any time in your App Store or Google Play settings.</p>
    </div>
</section>

<section class="alt">
    <div class="container narrow">
        <div class="notice">
            <p><strong>A first opinion, not a certificate.</strong> Autograph Identifier is built for quick screening: sorting an inherited collection, checking a listing before you bid, or deciding which items are worth sending to PSA/DNA, JSA or Beckett. It works best on clear photos of well-known signatures and will tell you when a signature is unclear instead of guessing. For expensive items, always get professional authentication.</p>
        </div>
    </div>
</section>

<section id="learn">
    <div class="container">
        <div class="section-head">
            <h2>Learn to authenticate autographs</h2>
            <p>Short, practical articles for collectors.</p>
        </div>
        <div class="grid grid-3">
{article_cards}
        </div>
    </div>
</section>

<section class="alt">
    <div class="container narrow">
        <div class="section-head"><h2>Frequently asked questions</h2></div>
        {faq_html(HOME_FAQ)}
    </div>
</section>

<section id="download" class="cta-band">
    <div class="container">
        <h2>Got an autograph you are not sure about?</h2>
        <p>Scan it now. Your first result is free.</p>
        {badges()}
        <p class="small">iPhone and iPad (iOS 17.5 or later) · Android · Free with optional Premium</p>
    </div>
</section>
"""
    schema = "\n    ".join([
        json_ld({
            "@context": "https://schema.org",
            "@type": "MobileApplication",
            "name": "Autograph Identifier",
            "description": "AI autograph identification and first-opinion authenticity assessment for collectors.",
            "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "iOS, Android",
            "image": f"{SITE}/assets/logo-512.png",
            "screenshot": [f"{SITE}/assets/screens/babe-ruth-result.jpg",
                           f"{SITE}/assets/screens/marilyn-monroe-result.jpg"],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "installUrl": [APP_STORE, PLAY_STORE],
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(RATING["value"]),
                "ratingCount": str(RATING["count"]),
            },
        }),
        json_ld({
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Autograph Identifier",
            "url": SITE + "/",
            "logo": f"{SITE}/assets/logo-512.png",
            "sameAs": [APP_STORE, PLAY_STORE],
            "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": EMAIL},
        }),
        json_ld({"@context": "https://schema.org", "@type": "WebSite", "name": "Autograph Identifier", "url": SITE + "/"}),
    ])
    write("/index.html", layout(
        "/",
        "Autograph Identifier: AI Autograph Authentication App",
        "Photograph any autograph and get the signer's name, an authenticity assessment and red flags in seconds. "
        "Free to download with 1 free scan, on iPhone and Android.",
        body, schema))


# ---------------------------------------------------------------- signature guides

def build_person(p):
    name = p["name"]
    path = f"/signatures/{p['slug']}/"
    title = f"{name} Autograph: Real vs Fake Signature Guide"
    desc = f"How to identify a genuine {name} autograph: signature characteristics, common fakes and how to verify it. {p['blurb']}"
    li = lambda items: "\n".join(f"<li>{i}</li>" for i in items)
    others = [o for o in PEOPLE if o["slug"] != p["slug"]]
    same = [o for o in others if o["category"] == p["category"]]
    related = (same + [o for o in others if o not in same])[:3]
    body = f"""
<div class="page-head">
    <div class="container narrow">
        <p class="crumbs"><a href="/">Home</a> › <a href="/signatures/">Signature guides</a> › {e(name)}</p>
        <h1>{e(name)} autograph: how to tell real from fake</h1>
        <p>{e(p['blurb'])}</p>
    </div>
</div>
<article class="prose">
    <div class="container narrow">
        {"".join(f"<p>{e(t)}</p>" for t in p["intro"])}

        <h2>What a genuine {e(name)} signature looks like</h2>
        <ul>
{li(p["traits"])}
        </ul>

        {cta_box(f"Have a {name} autograph?", "Check it with AI in seconds. Photograph the signature and get the identified name, an authenticity assessment and any red flags.")}

        <h2>Common fakes and red flags</h2>
        <ul>
{li(p["pitfalls"])}
        </ul>

        <h2>How to verify a {e(name)} autograph</h2>
        <ul>
{li(p["verify"])}
        </ul>
        <p>New to certification? Read <a href="/blog/psa-jsa-beckett-autograph-authentication/">PSA vs JSA vs Beckett explained</a> and our <a href="/blog/how-to-spot-a-fake-autograph/">checklist for spotting a fake autograph</a>.</p>

        <h2>{e(name)} autograph FAQ</h2>
        {faq_html(p["faq"])}

        <p class="disclaimer">This guide is general information for collectors, not an appraisal. Autograph Identifier gives an AI-generated first opinion, not a certificate of authenticity, and is not affiliated with or endorsed by {e(name)}, their estate or representatives, or any authentication company.</p>
    </div>
</article>
<div class="related">
    <div class="container">
        <h2>More signature guides</h2>
        <div class="grid grid-3" style="margin-top:18px">
{chr(10).join(person_card(o) for o in related)}
        </div>
    </div>
</div>
"""
    schema = "\n    ".join([
        json_ld({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "about": {"@type": "Thing", "name": f"{name} autograph"},
            "datePublished": "2026-11-17",
            "dateModified": TODAY,
            "author": {"@type": "Organization", "name": "Autograph Identifier", "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": "Autograph Identifier",
                          "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo-512.png"}},
            "mainEntityOfPage": SITE + path,
            "image": f"{SITE}/assets/og-image.png",
        }),
        crumb_schema([("Home", "/"), ("Signature guides", "/signatures/"), (name, path)]),
    ])
    write(path, layout(path, title, desc, body, schema, "article"))


def build_people_hub():
    body = f"""
<div class="page-head">
    <div class="container">
        <p class="crumbs"><a href="/">Home</a> › Signature guides</p>
        <h1>Autograph signature guides</h1>
        <p>What the genuine signature looks like, which fakes are common and how to verify it, for the most collected names in sports, music and history.</p>
    </div>
</div>
<section>
    <div class="container">
        <div class="grid grid-3">
{chr(10).join(person_card(p) for p in PEOPLE)}
        </div>
        {cta_box("Not sure whose signature you have?", "Photograph it and let the AI identify the signer and flag anything suspicious.")}
    </div>
</section>
"""
    schema = "\n    ".join([
        crumb_schema([("Home", "/"), ("Signature guides", "/signatures/")]),
        json_ld({
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": f"{p['name']} autograph guide",
                 "url": f"{SITE}/signatures/{p['slug']}/"}
                for i, p in enumerate(PEOPLE)
            ],
        }),
    ])
    write("/signatures/", layout(
        "/signatures/",
        "Autograph Signature Guides: Real vs Fake by Signer",
        "Signature guides for Michael Jordan, Babe Ruth, Mickey Mantle, The Beatles, Neil Armstrong and more: "
        "genuine characteristics, common fakes and how to verify.",
        body, schema))


# ---------------------------------------------------------------- blog

def build_article(a):
    path = f"/blog/{a['slug']}/"
    nice_date = date.fromisoformat(a["date"]).strftime("%B %-d, %Y")
    others = [o for o in ARTICLES if o["slug"] != a["slug"]]
    body = f"""
<div class="page-head">
    <div class="container narrow">
        <p class="crumbs"><a href="/">Home</a> › <a href="/blog/">Blog</a></p>
        <h1>{e(a['title'])}</h1>
        <p>{e(a['summary'])}</p>
    </div>
</div>
<article class="prose">
    <div class="container narrow">
        <p class="meta">Published {nice_date} · Autograph Identifier</p>
        {a['body']}
        {cta_box("Check an autograph with AI", "Photograph a signature and get the identified name, an authenticity assessment and any red flags in seconds.")}
        <p class="disclaimer">This article is general information for collectors, not an appraisal or legal advice. Autograph Identifier gives an AI-generated first opinion, not a certificate of authenticity, and is not affiliated with PSA, JSA, Beckett or Upper Deck.</p>
    </div>
</article>
<div class="related">
    <div class="container">
        <h2>Keep reading</h2>
        <div class="grid grid-3" style="margin-top:18px">
{chr(10).join(article_card(o) for o in others)}
<a class="card" href="/signatures/"><h3>Signature guides by signer</h3><p>Michael Jordan, Babe Ruth, The Beatles, Neil Armstrong and more.</p><span class="more">Browse guides →</span></a>
        </div>
    </div>
</div>
"""
    schema = "\n    ".join([
        json_ld({
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": a["title"],
            "description": a["desc"],
            "datePublished": a["date"],
            "dateModified": a["date"],
            "author": {"@type": "Organization", "name": "Autograph Identifier", "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": "Autograph Identifier",
                          "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo-512.png"}},
            "mainEntityOfPage": SITE + path,
            "image": f"{SITE}/assets/og-image.png",
        }),
        crumb_schema([("Home", "/"), ("Blog", "/blog/"), (a["title"], path)]),
    ])
    write(path, layout(path, a["title"], a["desc"], body, schema, "article"))


def build_blog_hub():
    body = f"""
<div class="page-head">
    <div class="container">
        <p class="crumbs"><a href="/">Home</a> › Blog</p>
        <h1>Autograph authentication blog</h1>
        <p>Practical guides for collectors: spotting fakes, understanding certification and knowing what you own.</p>
    </div>
</div>
<section>
    <div class="container">
        <div class="grid grid-3">
{chr(10).join(article_card(a) for a in ARTICLES)}
        </div>
        {cta_box("Check an autograph with AI", "Photograph a signature and get the identified name, an authenticity assessment and any red flags in seconds.")}
    </div>
</section>
"""
    write("/blog/", layout(
        "/blog/",
        "Autograph Authentication Blog for Collectors",
        "Guides for autograph collectors: how to spot a fake autograph, what PSA, JSA and Beckett certification means, "
        "and how to recognise autopen and secretarial signatures.",
        body, crumb_schema([("Home", "/"), ("Blog", "/blog/")])))


# ---------------------------------------------------------------- misc files

def build_sitemap():
    urls = [("/", "1.0", TODAY), ("/signatures/", "0.9", TODAY), ("/blog/", "0.8", TODAY)]
    urls += [(f"/signatures/{p['slug']}/", "0.8", TODAY) for p in PEOPLE]
    urls += [(f"/blog/{a['slug']}/", "0.7", a["date"]) for a in ARTICLES]
    urls += [("/privacy-policy.html", "0.2", TODAY), ("/terms-of-use.html", "0.2", TODAY)]
    rows = "\n".join(
        f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{mod}</lastmod>\n    <priority>{prio}</priority>\n  </url>"
        for path, prio, mod in urls)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n'
                          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n')


def build_404():
    body = f"""
<section style="text-align:center;padding:96px 0">
    <div class="container narrow">
        <h1 style="font-size:2.4rem;color:var(--ink);margin-bottom:12px">Page not found</h1>
        <p style="margin-bottom:28px">That page does not exist or has moved. Try one of these instead:</p>
        <div class="grid grid-3">
            <a class="card" href="/"><h3>Home</h3><p>What the app does and how to get it.</p></a>
            <a class="card" href="/signatures/"><h3>Signature guides</h3><p>Real vs fake, signer by signer.</p></a>
            <a class="card" href="/blog/"><h3>Blog</h3><p>Authentication basics for collectors.</p></a>
        </div>
    </div>
</section>
"""
    page = layout("/404.html", "Page Not Found | Autograph Identifier",
                  "The page you are looking for does not exist.", body)
    write("/404.html", page.replace('content="index, follow, max-image-preview:large, max-snippet:-1"',
                                    'content="noindex"'))


if __name__ == "__main__":
    build_home()
    build_people_hub()
    for person in PEOPLE:
        build_person(person)
    build_blog_hub()
    for article in ARTICLES:
        build_article(article)
    build_sitemap()
    build_404()
    print(f"Built {3 + len(PEOPLE) + len(ARTICLES)} pages · rating {RATING['value']} ({RATING['count']}) as of {RATING['fetched']}")
