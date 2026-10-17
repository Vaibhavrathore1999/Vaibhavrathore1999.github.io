---
layout: portfolio
title: "Curriculum vitae"
permalink: /cv/
eyebrow: "Research & experience"
description: "Academic inquiry and applied AI, in parallel."
redirect_from: [/resume, /cv-json/]
---

{% assign cv = site.data.cv %}
<div class="cv-toolbar"><a class="primary-link" href="{{ '/files/cv.pdf' | relative_url }}" download>Download CV <span class="meta">PDF ↓</span></a><p class="meta">Updated {{ cv.updated | date: '%d %b %Y' }}</p></div>
<p>{{ cv.basics.summary }}</p>
<div class="text-links">{% for profile in cv.basics.profiles %}<a href="{{ profile.url }}">{{ profile.network }}</a>{% endfor %}<a href="mailto:{{ cv.basics.email }}">Email</a></div>
<nav class="section-nav" aria-label="CV sections"><a href="#experience">Experience</a><a href="#education">Education</a><a href="#recognition">Recognition</a><a href="#cv-publications">Publications</a><a href="#service">Service</a></nav>

<section id="experience"><div class="section-heading"><h2>Experience</h2></div><div class="cv-timeline">{% for job in cv.work %}<article><p class="meta cv-date">{{ job.startDate | append: '-01' | date: '%b %Y' }} — {% if job.endDate == 'Present' %}Present{% else %}{{ job.endDate | append: '-01' | date: '%b %Y' }}{% endif %}</p><div><h3>{{ job.position }}</h3><p class="cv-org">{{ job.company }}</p><p>{{ job.summary }}</p></div></article>{% endfor %}</div></section>

<section id="education"><div class="section-heading"><h2>Education</h2></div><div class="cv-timeline">{% for item in cv.education limit:3 %}<article><p class="meta cv-date">{{ item.startDate }} — {{ item.endDate }}</p><div><h3>{{ item.studyType }} · {{ item.institution }}</h3><p>{{ item.area }}</p><p class="meta">CPI {{ item.gpa }}</p>{% if item.courses.size > 0 %}<details><summary>Selected coursework</summary><p>{{ item.courses | join: ' · ' }}</p></details>{% endif %}</div></article>{% endfor %}</div><details class="school-record"><summary>Earlier education</summary>{% for item in cv.education offset:3 %}<p>{{ item.studyType }} · {{ item.institution }} · {{ item.startDate }}–{{ item.endDate }} · {{ item.gpa }}</p>{% endfor %}</details></section>

<section id="recognition"><div class="section-heading"><h2>Recognition</h2></div>{% for award in cv.awards %}<article class="recognition"><p class="meta">{{ award.date | date: '%d %b %Y' }}</p><h3>{{ award.title }}</h3><p>{{ award.awarder }} · {{ award.summary }}</p></article>{% endfor %}{% for item in cv.achievements %}<p><strong>{{ item.title }}</strong> · {{ item.year }}<br>{{ item.summary }}</p>{% endfor %}</section>

<section id="cv-publications"><div class="section-heading"><h2>Publications &amp; accepted work</h2><a href="{{ '/publications/' | relative_url }}">Explore papers ↗</a></div>
  <h3 class="subheading">Conferences &amp; journals</h3>{% assign papers = site.data.research.published | where: 'group', 'main' %}{% for work in papers %}{% include publication-entry.html work=work compact=true %}{% endfor %}
  <h3 class="subheading">Workshops &amp; posters</h3>{% assign papers = site.data.research.published | where: 'group', 'workshop' %}{% for work in papers %}{% include publication-entry.html work=work compact=true %}{% endfor %}
</section>

<section id="service"><div class="section-heading"><h2>Teaching &amp; service</h2></div><div class="cv-columns"><div><h3>Teaching</h3>{% for item in cv.teaching %}<p><strong>{{ item.course }}</strong><br>{{ item.role }}, {{ item.institution }}<br><span class="meta">{{ item.date }}</span></p>{% endfor %}<h3>Mentoring</h3>{% for item in cv.mentoring %}<p>{{ item.role }}, {{ item.institution }}<br>{{ item.summary }}<br><span class="meta">{{ item.date }}</span></p>{% endfor %}</div><div><h3>Academic service</h3>{% for item in cv.service %}<p><strong>{{ item.name }}</strong><br>{{ item.role }} · {{ item.year }}</p>{% endfor %}</div></div></section>
<section><div class="section-heading"><h2>Skills &amp; interests</h2></div>{% for item in cv.skills %}<p>{{ item.keywords | join: ' · ' }}</p>{% endfor %}{% for item in cv.interests %}<p class="meta">{{ item.keywords | join: ' · ' }}</p>{% endfor %}</section>
