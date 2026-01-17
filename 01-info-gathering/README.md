# Information Gathering (theHarvester)

**Goal:** enumerate emails, people names, hosts, and subdomains for `beuth-hochschule.de`.

> Run only with permission.

## Commands (Kali)

```bash
# Some Kali images name it `theHarvester`, others `TheHarvester`
theHarvester -h || TheHarvester -h

# Try a couple of sources (Google is often rate-limited)
theHarvester -d beuth-hochschule.de -b bing -l 500 -f beuth_bing
# If you have API keys configured:
theHarvester -d beuth-hochschule.de -b bingapi -l 500 -f beuth_bingapi
```

## What to capture in your report

- **Email addresses found** (deduplicate)
- **Subdomains/hosts found** (and which source they came from)
- **People names** (if returned by sources like LinkedIn/Jigsaw)
- Screenshots / the generated `beuth_*.html` output

## Notes

- Treat the output as *leads*, not truth (verify before using).
- Avoid aggressive scraping settings (limits / pacing) to reduce rate limits.
