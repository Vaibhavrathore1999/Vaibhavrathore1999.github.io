---
layout: archive
title: "Research"
permalink: /projects/
author_profile: false
---

<p class="intro intro--small">I study how models transfer to unfamiliar domains, identify novel categories, and retain useful structure under practical constraints.</p>

## Research themes

<div class="theme-grid">
  <div><span>01</span><h3>Generalization</h3><p>Learning representations that remain reliable across unseen domains and distribution shifts.</p></div>
  <div><span>02</span><h3>Open worlds</h3><p>Recognizing known concepts while discovering categories absent from the training labels.</p></div>
  <div><span>03</span><h3>Geometry</h3><p>Using hyperbolic and structure-aware representations for hierarchical visual data.</p></div>
  <div><span>04</span><h3>Applied AI</h3><p>Building useful systems across Indic language technology, multimodal learning, and financial data.</p></div>
</div>

## Current work

<div class="research-list compact">
{% for work in site.data.research.ongoing %}
  <article class="research-item">
    <h3>{{ work.title }}</h3>
    <p>{{ work.summary }}</p>
  </article>
{% endfor %}
</div>

## Selected completed projects

<div class="research-list">
{% for work in site.data.research.published limit:4 %}
  <article class="research-item">
    <p class="research-meta">{{ work.venue }}</p>
    <h3>{{ work.title }}</h3>
    <p>{{ work.summary }}</p>
    <p class="research-links">{% for link in work.links %}<a href="{{ link.url }}">{{ link.label }}</a>{% unless forloop.last %}<span>·</span>{% endunless %}{% endfor %}</p>
  </article>
{% endfor %}
</div>

## Earlier projects

- **AI Support Assistant** — A retrieval-augmented support system built around product manuals and a QLoRA-tuned language model.
- **Kinector** — A text-conditioned 2D gesture generator using MediaPipe keypoints and a GRU pose model.
- **Medical Image Deblurring** — A scale-recurrent network with spatial-asymmetric attention for multimodal medical images.
- **Learning with Noisy Labels** — Vision Transformer experiments on CIFAR-100 with substantial label noise.
