#!/usr/bin/env python3
"""Assemble Phoenix Solutions pages from bodies/ into deployable HTML."""
import os, re

SITE = os.path.dirname(os.path.abspath(__file__))
BODIES = os.path.join(SITE, "bodies")

LOGO_SVG = """<svg class="logo-mark" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<path d="M20 3C17 8 12 10 9 10c4 2 7 2 10 1-2 3-6 5-10 5 5 2 9 1 12-1-1 5-5 9-9 10 6 0 10-3 12-7 1 6-1 11-5 15 6-3 9-8 9-14 2 3 2 7 1 10 3-4 4-9 2-14 3 1 5 3 6 6 0-5-2-9-6-12 3-1 5-1 8 0-3-3-7-4-11-3 1-3 3-5 6-6-5 0-9 3-11 7-1-3-1-5 0-7z" fill="#FF6A00"/>
</svg>"""

HEADER = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
<link rel="icon" type="image/svg+xml" href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="%231A1A1A"/><path d="M20 6C17.5 10 13.5 12 11 12c3.3 1.6 5.8 1.6 8.3.8-1.6 2.5-5 4.1-8.3 4.1 4.1 1.6 7.5.8 10-1-0.8 4.1-4.1 7.5-7.5 8.3 5 0 8.3-2.5 10-5.8.8 5-.8 9.1-4.1 12.4 5-2.5 7.5-6.6 7.5-11.6 1.6 2.5 1.6 5.8.8 8.3 2.5-3.3 3.3-7.5 1.6-11.6 2.5.8 4.1 2.5 5 5 0-4.1-1.6-7.5-5-10 2.5-.8 4.1-.8 6.6 0-2.5-2.5-5.8-3.3-9.1-2.5.8-2.5 2.5-4.1 5-5-4.1 0-7.5 2.5-9.1 5.8-.8-2.5-.8-4.1 0-5.8z" fill="%23FF6A00"/></svg>'>
</head>
<body{theme}>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="topbar">
    <div class="wrap">
      <div><a href="tel:+447460060032">+44 7460 060032</a> &nbsp;·&nbsp; <a href="mailto:info@phoenixsolutions.com">info@phoenixsolutions.com</a></div>
      <div class="accred">NICEIC Platinum · OZEV Authorised · MCS Certified · Tesla Powerwall Certified</div>
    </div>
  </div>
  <div class="wrap navbar">
    <a class="logo" href="index.html" aria-label="Phoenix Solutions home">
      __LOGO__
      <span class="logo-text">
        <span class="l1">PHO<span class="ebar" aria-hidden="true"></span>NIX</span>
        <span class="l2">SOLUTIONS</span>
      </span>
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <ul class="nav-links">
      <li><a href="index.html"{a_home}>Home</a></li>
      <li class="has-drop">
        <a href="index.html#services"{a_services}>Services</a>
        <ul class="dropdown">
          <li><a href="ev-charging.html"><span class="dot dot-ev"></span>EV Charging, Phoenix EV</a></li>
          <li><a href="solar.html"><span class="dot dot-solar"></span>Solar &amp; Battery, Phoenix Solar</a></li>
          <li><a href="smart-home.html"><span class="dot dot-smart"></span>Smart Home, Phoenix Smart</a></li>
          <li><a href="maintenance.html"><span class="dot dot-maint"></span>Compliance &amp; Maintenance</a></li>
        </ul>
      </li>
      <li><a href="projects.html"{a_projects}>Projects</a></li>
      <li><a href="about.html"{a_about}>About</a></li>
      <li><a href="contact.html"{a_contact}>Contact</a></li>
      <li class="nav-cta"><a class="btn btn-primary" href="quote.html">Request a Quote</a></li>
    </ul>
  </div>
</header>
<main id="main">
"""

FOOTER = """</main>
<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>{cta_h}</h2>
      <p>{cta_p}</p>
    </div>
    <div style="display:flex;gap:14px;flex-wrap:wrap">
      <a class="btn btn-white" href="quote.html">Request a Quote</a>
      <a class="btn btn-ghost" href="tel:+447460060032">Call +44 7460 060032</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="logo" href="index.html" aria-label="Phoenix Solutions home">
          __LOGO__
          <span class="logo-text">
            <span class="l1">PHO<span class="ebar" aria-hidden="true"></span>NIX</span>
            <span class="l2">SOLUTIONS</span>
          </span>
        </a>
        <p>Electrical engineering for the way we live now, EV charging, solar energy, smart buildings and certified compliance, delivered across London and the South East.</p>
        <div class="footer-accreds">
          <span>NICEIC Platinum</span><span>OZEV Authorised</span><span>MCS Certified</span><span>Tesla Powerwall</span>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="ev-charging.html">EV Charger Installation</a></li>
          <li><a href="solar.html">Solar PV &amp; Battery Storage</a></li>
          <li><a href="smart-home.html">Smart Home Technology</a></li>
          <li><a href="maintenance.html">EICR Reports &amp; Certificates</a></li>
          <li><a href="maintenance.html#fusebox">Fuse Box Upgrades</a></li>
          <li><a href="maintenance.html#fire">Fire Alarms &amp; Emergency Lighting</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Phoenix Solutions</a></li>
          <li><a href="projects.html">Recent Projects</a></li>
          <li><a href="quote.html">Request a Quote</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li>Flat 17 Bron Court, Brondesbury Road,<br>London NW6 6AU</li>
          <li><a href="tel:+447460060032">+44 7460 060032</a></li>
          <li><a href="mailto:info@phoenixsolutions.com">info@phoenixsolutions.com</a></li>
          <li>Mon-Fri 8:00-18:00 · Sat 9:00-14:00</li>
          <li>24/7 emergency call-out for existing clients</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© <span id="year"></span> Phoenix Solutions Ltd. All rights reserved.</div>
      <div>Registered in England &amp; Wales · phoenix-solutionsuk.com</div>
    </div>
  </div>
</footer>
<script src="js/main.js"></script>
</body>
</html>
"""

PAGES = {
  "index.html": dict(title="Phoenix Solutions | Electrical Engineering, EV Charging, Solar & Smart Buildings, London",
      desc="NICEIC Platinum electrical contractors in London. EV charger installation, solar PV and battery storage, smart home technology, EICR reports, fuse box upgrades and fire safety systems.",
      theme="", active="home",
      cta_h="Ready to power your next project?",
      cta_p="Tell us what you need and we'll come back within one working day with a clear, fixed-price quotation."),
  "ev-charging.html": dict(title="EV Charger Installation London | Phoenix EV, OZEV Authorised Installers",
      desc="Home and workplace EV charger installation by OZEV-authorised engineers. Tethered and untethered 7kW-22kW units, smart charging, load management and full electrical certification.",
      theme=' data-theme="ev"', active="services",
      cta_h="Charge at home from tomorrow morning.",
      cta_p="Send us a photo of your fuse board and parking spot, most home surveys are completed remotely and installed within a week."),
  "solar.html": dict(title="Solar Panel & Battery Storage Installation | Phoenix Solar, MCS Certified",
      desc="MCS-certified solar PV design and installation with battery storage. In-roof and on-roof systems, Tesla Powerwall, bird protection, SEG export registration and 25-year panel warranties.",
      theme=' data-theme="solar"', active="services",
      cta_h="Start generating your own electricity.",
      cta_p="Get a free desktop solar assessment for your roof, with modelled generation figures and payback period, within 48 hours."),
  "smart-home.html": dict(title="Smart Home Installation London | Phoenix Smart, Lighting, Heating, Security",
      desc="Smart home design and installation: intelligent lighting, heating zones, whole-home audio, video entry, CCTV, access control and integrated fire and security systems.",
      theme=' data-theme="smart"', active="services",
      cta_h="Make your home work around you.",
      cta_p="Book a smart home design consultation, we'll map out a system you can control from one app, installed by qualified electricians."),
  "maintenance.html": dict(title="EICR Reports, Fuse Box Upgrades & Fire Alarm Systems | Phoenix Maintenance",
      desc="Electrical compliance for homeowners, landlords and businesses: EICR condition reports, consumer unit upgrades, emergency light testing, fire alarm systems, PAT testing and 24/7 maintenance.",
      theme=' data-theme="maintenance"', active="services",
      cta_h="Stay compliant. Stay safe. Stay open.",
      cta_p="Book an EICR, fire alarm service or emergency lighting test, certificates issued digitally, usually within 24 hours of the visit."),
  "projects.html": dict(title="Recent Projects | Phoenix Solutions, EV, Solar, Smart & Compliance Case Studies",
      desc="A selection of recent Phoenix Solutions installations across London and the South East: EV charging hubs, solar and battery systems, smart homes and commercial compliance programmes.",
      theme="", active="projects",
      cta_h="Your project could be next.",
      cta_p="From a single home charger to a full commercial fit-out, tell us what you're planning and we'll price it properly."),
  "about.html": dict(title="About Phoenix Solutions | NICEIC Platinum Electrical Engineers, London",
      desc="Phoenix Solutions is a London electrical engineering company led by CEO Rabih Srour, specialising in EV charging, solar energy, smart buildings and electrical compliance.",
      theme="", active="about",
      cta_h="Work with engineers who sweat the details.",
      cta_p="Every job certified, every cable clipped straight, every client called back. That's the Phoenix standard."),
  "contact.html": dict(title="Contact Phoenix Solutions | London Electrical Contractors",
      desc="Contact Phoenix Solutions: call +44 7460 060032, email info@phoenixsolutions.com or visit us at Bron Court, Brondesbury Road, London NW6 6AU.",
      theme="", active="contact",
      cta_h="Prefer a fixed price in writing?",
      cta_p="Use our quote form and we'll respond within one working day with a clear, itemised quotation."),
  "quote.html": dict(title="Request a Quote | Phoenix Solutions",
      desc="Request a free, fixed-price quotation for EV charging, solar, smart home or electrical compliance work. We respond within one working day.",
      theme="", active="quote",
      cta_h="Not sure what you need yet?",
      cta_p="Call us for a no-obligation chat, we'll help you scope the job before you commit to anything."),
  "404.html": dict(title="Page not found | Phoenix Solutions",
      desc="The page you were looking for could not be found.",
      theme="", active="",
      cta_h="Let's get you back on track.",
      cta_p="Head to the homepage or request a quote, or call us and we'll point you the right way."),
}

def build():
    for fname, meta in PAGES.items():
        body_path = os.path.join(BODIES, fname)
        with open(body_path) as f:
            body = f.read()
        act = {k: "" for k in ("a_home","a_services","a_projects","a_about","a_contact")}
        if meta["active"]:
            key = "a_" + meta["active"]
            if key in act:
                act[key] = ' class="active"'
        head = HEADER.format(title=meta["title"], desc=meta["desc"], theme=meta["theme"], **act)
        foot = FOOTER.format(cta_h=meta["cta_h"], cta_p=meta["cta_p"])
        html = (head + body + foot).replace("__LOGO__", LOGO_SVG)
        with open(os.path.join(SITE, fname), "w") as f:
            f.write(html)
        print("built", fname, len(html), "bytes")

if __name__ == "__main__":
    build()
