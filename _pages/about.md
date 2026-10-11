---
layout: single
title: "Vaibhav Rathore"
permalink: /
author_profile: false
redirect_from:
  - /about/
  - /about.html
---

<p class="eyebrow">AI researcher & engineer · Mumbai, India</p>

<p class="intro">I build learning systems that generalize beyond their training data—across domains, categories, languages, and real-world constraints.</p>

I am a Senior AI Data Scientist at Motilal Oswal Financial Services and a Ph.D. Scholar at CSRE, IIT Bombay. My research sits at the intersection of domain generalization, open-world recognition, representation learning, and applied AI.

<p class="text-links"><a href="mailto:vaibhav.rathor.in@gmail.com">Email</a> <a href="https://scholar.google.co.in/citations?hl=en&user=VH1wZJkAAAAJ">Google Scholar</a> <a href="https://github.com/Vaibhavrathore1999">GitHub</a> <a href="https://www.linkedin.com/in/vaibhav-rathore-ab696b188/">LinkedIn</a></p>

## Selected work

<div class="research-list">
{% for work in site.data.research.published limit:4 %}
  <article class="research-item">
    <p class="research-meta">{{ work.venue }} · {{ work.status }}</p>
    <h3>{{ work.title }}</h3>
    <p>{{ work.summary }}</p>
    <p class="research-links">{% for link in work.links %}<a href="{{ link.url }}">{{ link.label }}</a>{% unless forloop.last %}<span>·</span>{% endunless %}{% endfor %}</p>
  </article>
{% endfor %}
</div>

<p class="section-link"><a href="{{ '/publications/' | relative_url }}">View all publications →</a></p>

## Ongoing research

<div class="research-list compact">
{% for work in site.data.research.ongoing %}
  <article class="research-item">
    <h3>{{ work.title }}</h3>
    <p>{{ work.summary }}</p>
  </article>
{% endfor %}
</div>

## Current roles

<div class="timeline-list">
  <div><span>2025—Now</span><p><strong>Senior AI Data Scientist</strong><br>Motilal Oswal Financial Services</p></div>
  <div><span>2026—Now</span><p><strong>Ph.D. Scholar</strong><br>CSRE, IIT Bombay</p></div>
  <div><span>2023—2025</span><p><strong>M.S. by Research</strong><br>AI & Data Science, C-MInDS, IIT Bombay</p></div>
</div>

## Professional service

Reviewer or program committee member for AAAI, AISTATS, ICVGIP, the NeurIPS Position Paper Track, and the International Journal of Computer Vision.

## Contact

I am open to thoughtful research collaborations. If our interests overlap, [send me a short note](mailto:vaibhav.rathor.in@gmail.com) with the problem you are exploring.
