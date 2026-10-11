---
layout: single
title: "Vaibhav Rathore"
permalink: /
author_profile: false
redirect_from:
  - /about/
  - /about.html
---

<div class="profile-intro">
  <div class="profile-copy">
    <p class="eyebrow">AI researcher &amp; engineer · Mumbai, India</p>
    <p class="intro">I build learning systems that generalize beyond their training data—across domains, categories, languages, and real-world constraints.</p>
    <p>I am a Senior AI Data Scientist at Motilal Oswal Financial Services and a Ph.D. Scholar at CSRE, IIT Bombay. My research sits at the intersection of domain generalization, open-world recognition, representation learning, and applied AI.</p>
    <p class="text-links"><a href="mailto:vaibhav.rathor.in@gmail.com">Email</a> <a href="https://scholar.google.co.in/citations?hl=en&user=VH1wZJkAAAAJ">Google Scholar</a> <a href="https://github.com/Vaibhavrathore1999">GitHub</a> <a href="https://www.linkedin.com/in/vaibhav-rathore-ab696b188/">LinkedIn</a></p>
  </div>
  <figure class="profile-portrait">
    <img src="{{ '/images/profile.png' | relative_url }}" alt="Vaibhav Rathore" fetchpriority="high">
  </figure>
</div>

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
{% for work in site.data.research.ongoing limit:4 %}
  <article class="research-item">
    <h3>{{ work.title }}</h3>
    <p>{{ work.summary }}</p>
  </article>
{% endfor %}
</div>

<p class="section-link"><a href="{{ '/projects/' | relative_url }}">View all current research →</a></p>

## Journey

<p class="section-note">Selected milestones across research, education, and industry.</p>

<div class="journey-timeline">
{% for milestone in site.data.timeline %}
  <article class="journey-item">
    <div class="journey-year">{{ milestone.year }}</div>
    <div class="journey-content">
      <p class="journey-type">{{ milestone.type }}</p>
      <h3>{{ milestone.title }}</h3>
      <p>{{ milestone.summary }}</p>
      {% if milestone.link %}<p class="journey-link"><a href="{{ milestone.link | relative_url }}">{{ milestone.link_label }} →</a></p>{% endif %}
    </div>
  </article>
{% endfor %}
</div>

## Professional service

Reviewer or program committee member for AAAI, AISTATS, ICVGIP, the NeurIPS Position Paper Track, and the International Journal of Computer Vision.

## Contact

I am open to thoughtful research collaborations. If our interests overlap, [send me a short note](mailto:vaibhav.rathor.in@gmail.com) with the problem you are exploring.
