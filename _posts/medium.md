---
layout: single
title: "My Medium Articles"
permalink: /medium/
author_profile: true
---

## 📝 My Medium Articles
Here is an automatically updated feed of all the articles I publish on Medium.

---

{% assign feed_url = "https://medium.com/feed/@vaibhav.rathor.in" %}
{% capture xml %}{{ feed_url | fetch }}{% endcapture %}
{% assign items = xml | split:"<item>" %}

{% for item in items offset:1 %}
  {% assign title = item | split:"<title>" | last | split:"</title>" | first %}
  {% assign link = item | split:"<link>" | last | split:"</link>" | first %}
  {% assign pubdate = item | split:"<pubDate>" | last | split:"</pubDate>" | first %}
  {% assign description = item | split:"<description>" | last | split:"</description>" | first %}
  
### 🔹 {{ title }}
📅 {{ pubdate | date: "%B %-d, %Y" }}  
👉 [Read on Medium]({{ link }})

---

{% endfor %}
