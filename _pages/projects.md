---
layout: portfolio
title: "Research"
permalink: /projects/
eyebrow: "Questions I keep coming back to"
description: "How can learning systems recognize what they know, discover what they don’t, and remain useful when the world changes?"
---

<section class="research-themes" aria-label="Research themes">
  <details open><summary><span class="section-number">01</span> Generalization &amp; open worlds</summary><p>Recognizing known concepts while discovering new categories in unfamiliar domains. I work on representations and adaptation strategies that connect domain generalization with generalized category discovery.</p><a href="{{ '/publications/' | relative_url }}#dg-gcd">DG-GCD ↗</a> <a href="{{ '/publications/' | relative_url }}#hidisc">HiDISC ↗</a></details>
  <details><summary><span class="section-number">02</span> Geometry &amp; structure</summary><p>Hierarchies are everywhere—from geographic scenes to visual categories. I explore hyperbolic representations that make room for these structures, including open-world remote sensing.</p><a href="{{ '/publications/' | relative_url }}#helios">HElIOS ↗</a></details>
  <details><summary><span class="section-number">03</span> Language &amp; multimodal learning</summary><p>How we represent language affects what models retain and how they behave. My work spans morphology-aware Indic tokenization, multilingual interventions, and medical question answering across text and images.</p><a href="{{ '/publications/' | relative_url }}#sutra">SuTRA ↗</a> <a href="{{ '/publications/' | relative_url }}#beyond-accuracy">Beyond Accuracy ↗</a></details>
  <details><summary><span class="section-number">04</span> AI in financial systems</summary><p>At Motilal Oswal, I study structured financial generation, time-series representations, and the implications of agents sharing foundation models. Only public-safe research details are shared here.</p><a href="{{ '/publications/' | relative_url }}#candlediff">CandleDiff ↗</a> <a href="{{ '/publications/' | relative_url }}#many-agents">Many Agents, Few Minds ↗</a></details>
</section>

<section class="geometry-demo" data-geometry aria-labelledby="geometry-title">
  <div class="section-heading"><h2 id="geometry-title">A little geometric intuition</h2><span class="meta">Interactive notebook</span></div>
  <p>In a Euclidean plane, circles grow linearly with radius. In a hyperbolic plane, their circumference grows exponentially at large distances—one reason to explore this geometry for branching hierarchies.</p>
  <div class="geometry-controls" hidden><label for="geometry-radius">Distance from the origin <output id="geometry-value">2.0</output></label><input id="geometry-radius" type="range" min="0.5" max="4" step="0.1" value="2" aria-describedby="geometry-explanation"></div>
  <div class="geometry-plots">
    <figure><svg viewBox="0 0 240 240" role="img" aria-labelledby="euclid-label"><title id="euclid-label">Euclidean plane: a circle at distance 2 from the origin</title><path class="axes" d="M10 120H230M120 10V230"/><circle class="radius-ring" id="euclid-ring" cx="120" cy="120" r="50"/><circle class="origin" cx="120" cy="120" r="3"/></svg><figcaption>Euclidean plane<span id="euclid-metric">Circumference: 12.57</span></figcaption></figure>
    <figure><svg viewBox="0 0 240 240" role="img" aria-labelledby="hyperbolic-label"><title id="hyperbolic-label">Poincaré disk: a circle at hyperbolic distance 2 from the origin</title><circle class="disk-boundary" cx="120" cy="120" r="100"/><path class="axes" d="M20 120H220M120 20V220"/><circle class="radius-ring" id="hyperbolic-ring" cx="120" cy="120" r="76.1594"/><circle class="origin" cx="120" cy="120" r="3"/></svg><figcaption>Poincaré disk<span id="hyperbolic-metric">Circumference: 22.79</span></figcaption></figure>
  </div>
  <p class="meta" id="geometry-explanation">An illustration, not experimental results. Curvature −1; circumferences are 2πr and 2πsinh(r). The disk maps distance r to radius tanh(r/2); its boundary is infinitely far away. Screen sizes are not metric distances.</p>
  <noscript><p class="meta">The illustration shows r = 2. Enable JavaScript to change the radius.</p></noscript>
</section>

<section id="ongoing" aria-labelledby="ongoing-title">
  <div class="section-heading"><h2 id="ongoing-title">Ongoing research</h2></div>
  <p class="section-intro">Current questions and collaborations. Submission venues, review details, and private manuscript links are intentionally omitted.</p>
  {% for work in site.data.research.ongoing %}<article class="publication ongoing-work"><h3>{{ work.title | escape }}</h3><p class="authors">{{ work.authors | escape | replace: 'Vaibhav Rathore', '<strong>Vaibhav Rathore</strong>' }}</p><p>{{ work.summary | escape }}</p></article>{% endfor %}
</section>
<details class="earlier-work"><summary>Earlier explorations</summary>
  <h3>AI Support Assistant</h3><p>A retrieval-augmented support system built around product manuals and a QLoRA-tuned language model.</p>
  <h3>Kinector</h3><p>Text-conditioned 2D gesture generation using MediaPipe keypoints and a GRU pose model.</p>
  <h3>Medical Image Deblurring</h3><p>A scale-recurrent network with spatial-asymmetric attention for multimodal medical images.</p>
  <h3>Learning with Noisy Labels</h3><p>Vision Transformer experiments on CIFAR-100 with substantial label noise.</p>
</details>
