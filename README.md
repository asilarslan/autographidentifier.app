# autographidentifier.app

Website for the Autograph Identifier app ([App Store](https://apps.apple.com/app/autograph-identifier/id6749822952) · [Google Play](https://play.google.com/store/apps/details?id=com.autographidentifier)), served by GitHub Pages.

The pages are generated, so edit the sources and rebuild:

```
python3 build.py            # rebuild every page
python3 build.py --refresh  # also update the App Store rating shown on the site
```

- `src/people.py`: signature guides, one entry per `/signatures/<slug>/` page
- `src/articles.py`: blog articles, one entry per `/blog/<slug>/` page
- `build.py`: home page copy, shared layout, sitemap
- `assets/`: stylesheet, logos, store badges and app screenshots

Commit the generated HTML together with the source change. `privacy-policy.html` and `terms-of-use.html` are maintained by hand.
