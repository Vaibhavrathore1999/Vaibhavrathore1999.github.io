---
layout: portfolio
title: "Vaibhav Rathore"
permalink: /
home: true
description: "AI researcher at IIT Bombay and Motilal Oswal. Exploring generalization, open-world learning, and AI for real-world systems."
redirect_from: [/about/, /about.html]
---

<section class="hero" aria-labelledby="intro-title">
  <div>
    <p class="eyebrow">Research, curiosity &amp; things that work</p>
    <h1 id="intro-title">Vaibhav<br>Rathore<span class="wordmark-dot">.</span></h1>
    <p class="hero-statement">Learning beyond<br>the familiar.</p>
  </div>
  <figure class="portrait"><img src="{{ '/images/profile.png' | relative_url }}" alt="Vaibhav Rathore" width="210" height="252" fetchpriority="high"><figcaption>AI researcher &amp; engineer<br>Mumbai, India</figcaption></figure>
</section>
<div class="intro-copy">
  <p>I build learning systems that generalize beyond their training data—across domains, categories, languages, and real-world constraints.</p>
  <div class="roles"><p><span>Academic research</span>Ph.D. Scholar · IIT Bombay</p><p><span>Industry research</span>Senior AI Data Scientist · MOFSL</p></div>
  <div class="text-links"><a href="mailto:{{ site.data.cv.basics.email }}">Email</a><a href="{{ site.author.googlescholar }}">Scholar</a><a href="https://github.com/Vaibhavrathore1999">GitHub</a><a href="{{ site.author.linkedin }}">LinkedIn</a><a href="{{ '/cv/' | relative_url }}">CV ↗</a></div>
</div>

<aside class="now-block" aria-labelledby="now-title">
  <div><h2 id="now-title">Now</h2><p class="meta">Updated {{ site.data.home.updated | date: '%d %b %Y' }}</p></div>
  <div>{% for line in site.data.home.now %}<p>{{ line }}</p>{% endfor %}</div>
</aside>

<section aria-labelledby="selected-title">
  <div class="section-heading"><h2 id="selected-title"><span class="section-number">01</span> Selected work</h2><a href="{{ '/publications/' | relative_url }}">All publications ↗</a></div>
  <div class="featured-grid">
  {% for id in site.data.home.featured %}{% assign work = site.data.research.published | where: 'id', id | first %}
    <article class="featured-work">
      <p class="meta">{{ work.venue }} · {{ work.status }}</p>
      <h3><a href="{{ '/publications/' | relative_url }}#{{ work.id }}">{{ work.title }}</a></h3>
      <p>{{ work.summary }}</p>
      <a class="work-link" href="{{ '/publications/' | relative_url }}#{{ work.id }}">Explore work <span aria-hidden="true">↗</span><span class="sr-only">: {{ work.title }}</span></a>
    </article>
  {% endfor %}
  </div>
</section>

<section aria-labelledby="recent-title">
  <div class="section-heading"><h2 id="recent-title"><span class="section-number">02</span> Recent milestones</h2><a href="#journey">Full journey ↓</a></div>
  <div class="recent-list">{% assign recent = site.data.timeline | where: 'recent', true %}{% for item in recent limit:3 %}<div class="recent-item"><span class="meta">{{ item.year }}</span>{% include journey-item.html item=item %}</div>{% endfor %}</div>
</section>

<section id="journey" aria-labelledby="journey-title">
  <div class="section-heading"><h2 id="journey-title"><span class="section-number">03</span> A path into research</h2></div>
  <p class="section-intro">From mechanical engineering to learning systems. The work, people, and milestones along the way.</p>
  {% assign years = site.data.timeline | group_by: 'year' %}
  <div class="journey">{% for year in years %}<details class="journey-year" {% if forloop.first %}open{% endif %}><summary>{{ year.name }}<span>{{ year.items.size }} milestones</span></summary><div class="journey-events">{% for item in year.items %}{% include journey-item.html item=item %}{% endfor %}</div></details>{% endfor %}</div>
</section>

<section class="contact-section" aria-labelledby="contact-title">
  <p class="eyebrow">Start a conversation</p>
  <h2 id="contact-title">Good questions welcome.</h2>
  <p>Interested in open-world learning, geometric representations, multilingual AI, or financial machine learning? I’m open to thoughtful research collaborations.</p>
  <a class="contact-link" href="mailto:{{ site.data.cv.basics.email }}">Say hello ↗</a>
</section>
