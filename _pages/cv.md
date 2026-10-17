---
layout: archive
title: "CV"
permalink: /cv/
author_profile: false
redirect_from:
  - /resume
---

<p class="intro intro--small">AI researcher and engineer working on learning systems that generalize across domains, categories, languages, and real-world constraints.</p>

<p class="text-links"><a href="mailto:vaibhav.rathor.in@gmail.com">Email</a> <a href="https://scholar.google.co.in/citations?hl=en&user=VH1wZJkAAAAJ">Google Scholar</a> <a href="https://github.com/Vaibhavrathore1999">GitHub</a> <a href="https://www.linkedin.com/in/vaibhav-rathore-ab696b188/">LinkedIn</a> <a href="https://orcid.org/0009-0007-0603-4462">ORCID</a></p>

## Experience

<div class="cv-timeline">
  <article><div class="cv-date">2025—Now</div><div><h3>Senior AI Data Scientist</h3><p class="cv-org">Motilal Oswal Financial Services · AI Research</p><p>Applied and foundational AI for the Indian context, including financial time-series modeling, Indic language technology, and production ML systems. Public details remain high-level because the work is proprietary.</p></div></article>
  <article><div class="cv-date">2025</div><div><h3>Research Intern</h3><p class="cv-org">Motilal Oswal Financial Services</p><p>Evaluated lip-sync and Gaussian Splatting approaches for high-fidelity synchronization and controllable 3D avatars.</p></div></article>
  <article><div class="cv-date">2025</div><div><h3>Research Intern</h3><p class="cv-org">Sony Research India · Vehant Technologies</p><p>Worked on 3D lip synchronization, pedestrian attribute recognition, hyperbolic embeddings, attribute graphs, and domain shift.</p></div></article>
  <article><div class="cv-date">2024</div><div><h3>Research &amp; Development Intern</h3><p class="cv-org">Clinical AI Assistance</p><p>Fine-tuned language models with LoRA and developed multimodal medical question answering systems.</p></div></article>
  <article><div class="cv-date">2022—23</div><div><h3>Graduate Engineer Trainee</h3><p class="cv-org">Reliance Industries</p><p>Worked on predictive maintenance and operational analytics.</p></div></article>
</div>

## Education

<div class="cv-timeline">
  <article><div class="cv-date">2026—Now</div><div><h3>Ph.D. Scholar · CSRE, IIT Bombay</h3><p>CPI: 9.00</p></div></article>
  <article><div class="cv-date">2023—25</div><div><h3>M.S. by Research · AI &amp; Data Science, C-MInDS, IIT Bombay</h3><p>Completed with CPI: 9.31.</p></div></article>
  <article><div class="cv-date">2018—22</div><div><h3>B.Tech. · Mechanical Engineering, MNNIT Allahabad</h3><p>CPI: 9.10.</p></div></article>
</div>

## Publications

<div class="cv-publication-list">
{% for work in site.data.research.published %}
  <article>
    <p class="research-meta">{{ work.venue }} · {{ work.status }}</p>
    <h3>{{ work.title }}</h3>
    {% if work.affiliation %}<p class="research-affiliation">{{ work.affiliation }}</p>{% endif %}
    {% if work.links.size > 0 %}<p>{% for link in work.links %}<a href="{{ link.url }}">{{ link.label }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}</p>{% endif %}
  </article>
{% endfor %}
</div>

<p class="section-link"><a href="{{ '/projects/' | relative_url }}">Ongoing research is listed on the Research page →</a></p>

## Recognition

<div class="cv-facts">
  <div><span>2026</span><strong>Award for Excellence in Research</strong><p>C-MInDS, IIT Bombay</p></div>
  <div><span>2022</span><strong>GATE: 97.84 percentile</strong><p>Engineering Sciences (XE); 96 percentile in Mechanical Engineering (ME)</p></div>
  <div><span>2018</span><strong>Top 1 percentile</strong><p>JEE Main</p></div>
</div>

## Teaching &amp; service

<div class="cv-two-column">
  <div><h3>Teaching</h3><p>Teaching Assistant, IIT Bombay — DS 303: Introduction to Machine Learning; e-PGD: Python Programming.</p></div>
  <div><h3>Service</h3><p>Reviewer or program committee member for AAAI, AISTATS, ICVGIP, the NeurIPS Position Paper Track, and the International Journal of Computer Vision.</p></div>
</div>

## Skills

<p class="skill-line">Python · C++ · PyTorch · TensorFlow · scikit-learn · OpenCV · Hugging Face · Gaussian Splatting · Indic NLP · financial time-series modeling · production ML systems</p>
