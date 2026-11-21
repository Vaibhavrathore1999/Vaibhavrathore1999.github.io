---
layout: portfolio
title: "Vaibhav Rathore"
permalink: /
home: true
description: "AI researcher at IIT Bombay and Motilal Oswal. Exploring generalization, open-world learning, and AI for real-world systems."
redirect_from: [/about/, /about.html]
---

<section class="academic-intro" aria-labelledby="intro-title">
  <div>
    <h1 id="intro-title">Vaibhav Rathore</h1>
    <p class="intro-role">Ph.D. Scholar, IIT Bombay · Senior AI Data Scientist, MOFSL</p>
    <p>I am a Ph.D. scholar at IIT Bombay and a Senior AI Data Scientist at Motilal Oswal Financial Services. I completed my M.S. by Research in AI and Data Science at C-MInDS, IIT Bombay, after studying Mechanical Engineering at MNNIT Allahabad.</p>
    <p>My research focuses on learning systems that generalize across domains and discover new categories. I also work on multilingual models, multimodal learning, and financial AI.</p>
    <div class="text-links"><a href="{{ site.resume_url | relative_url }}" download>CV (PDF)</a><a href="mailto:{{ site.data.cv.basics.email }}">Email</a><a href="{{ site.author.googlescholar }}">Google Scholar</a><a href="https://github.com/Vaibhavrathore1999">GitHub</a><a href="{{ site.author.linkedin }}">LinkedIn</a></div>
  </div>
  <figure class="portrait"><img src="{{ '/images/profile.png' | relative_url }}" alt="Vaibhav Rathore" width="210" height="252" fetchpriority="high"></figure>
</section>

<section id="news" class="home-section" aria-labelledby="news-title">
  <h2 id="news-title">News</h2>
  <ul class="news-list">
    {% assign recent = site.data.timeline | where: 'recent', true %}{% for item in recent reversed %}<li><span class="meta">{{ item.year }}</span><span>{% if item.link %}<a href="{{ item.link | relative_url }}">{{ item.title }}</a>{% else %}{{ item.title }}{% endif %}.</span></li>{% endfor %}
  </ul>
</section>

<section id="publications" class="home-section" aria-labelledby="publications-title">
  <h2 id="publications-title">Publications</h2>
  <p class="section-intro">Published and accepted work. See also <a href="{{ site.author.googlescholar }}">Google Scholar</a>.</p>
  <ol class="simple-publications">
    {% for work in site.data.research.published %}
    <li id="{{ work.id }}">
      <h3>{% if work.links.size > 0 %}<a href="{{ work.links.first.url }}">{{ work.title | escape }}</a>{% else %}{{ work.title | escape }}{% endif %}</h3>
      <p class="authors">{{ work.authors | escape | replace: 'Vaibhav Rathore', '<strong>Vaibhav Rathore</strong>' }}</p>
      <p class="publication-venue">{{ work.venue | escape }} · {{ work.status }}{% if work.note %} · {{ work.note }}{% endif %}</p>
      {% if work.links.size > 0 %}<div class="text-links">{% for link in work.links %}<a href="{{ link.url }}">{{ link.label }}</a>{% endfor %}</div>{% endif %}
    </li>
    {% endfor %}
  </ol>
  <p class="section-intro"><a href="{{ '/projects/' | relative_url }}">Research themes &amp; ongoing projects →</a></p>
</section>

<section id="blog" class="home-section" aria-labelledby="blog-title">
  <h2 id="blog-title">Blog</h2>
  <ul class="simple-blog">{% assign native_posts = site.posts | where: 'native_article', true %}{% for post in native_posts limit:2 %}<li><a href="{{ post.url | relative_url }}">{{ post.title }}</a><p>{{ post.excerpt }}</p></li>{% endfor %}{% for article in site.data.writing limit:4 %}<li><a href="{{ article.url }}">{{ article.title }}</a><p>{{ article.summary | capitalize }}</p></li>{% endfor %}</ul>
  <a href="{{ '/medium/' | relative_url }}">All writing →</a>
</section>

<section id="experience" class="home-section" aria-labelledby="experience-title">
  <h2 id="experience-title">Experience</h2>
  <ul class="simple-experience">{% for job in site.data.cv.work %}<li><p class="meta">{{ job.startDate | append: '-01' | date: '%b %Y' }} – {% if job.endDate == 'Present' %}Present{% else %}{{ job.endDate | append: '-01' | date: '%b %Y' }}{% endif %}</p><div><h3>{{ job.position }}</h3><p>{{ job.company }}</p></div></li>{% endfor %}</ul>
</section>

<section id="education" class="home-section" aria-labelledby="education-title">
  <h2 id="education-title">Education</h2>
  <ul class="simple-experience">{% for item in site.data.cv.education limit:3 %}<li><p class="meta">{{ item.startDate }} – {{ item.endDate }}</p><div><h3>{{ item.studyType }} · {{ item.institution }}</h3><p>{{ item.area }}</p></div></li>{% endfor %}</ul>
</section>

<section id="awards" class="home-section" aria-labelledby="awards-title">
  <h2 id="awards-title">Awards</h2>
  {% for award in site.data.cv.awards %}<p>{{ award.date | date: '%Y' }} · <strong>{{ award.title }}</strong>, {{ award.awarder }}.</p>{% endfor %}
  <p><a href="{{ '/cv/' | relative_url }}">Full academic CV</a> · <a href="{{ site.resume_url | relative_url }}" download>Download resume (PDF)</a></p>
</section>
