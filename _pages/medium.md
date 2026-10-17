---
layout: portfolio
title: "Writing"
permalink: /medium/
eyebrow: "Notes from the learning process"
description: "Accessible explanations of machine learning, vision, and the mathematics underneath."
---

<div data-filter-list="writing">
  <form class="filter-bar" data-filters hidden><label>Explore a topic<select name="topic"><option value="">All topics</option><option value="foundations">Learning foundations</option><option value="mathematics">Mathematics</option><option value="vision">Computer vision</option></select></label><button type="reset" class="reset-button">Reset</button><p class="meta filter-count" aria-live="polite" role="status"></p></form>
  {% for article in site.data.writing %}<article class="writing-row" data-filter-item data-topic="{{ article.topic }}"><p class="meta">{{ article.topic | capitalize }} · On Medium</p><h2><a href="{{ article.url }}">{{ article.title }} ↗</a></h2><p>{{ article.summary | capitalize }}</p></article>{% endfor %}
  <p class="empty-state" hidden>No articles match this topic. Reset to browse all writing.</p>
</div>
<aside class="end-note"><h2>More notes, as I go</h2><p>Find the full archive and new articles on <a href="https://medium.com/@vaibhav.rathor.in">my Medium profile ↗</a>.</p></aside>
