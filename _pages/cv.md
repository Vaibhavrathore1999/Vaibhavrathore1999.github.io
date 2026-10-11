---
layout: archive
title: "CV"
permalink: /cv/
author_profile: false
redirect_from:
  - /resume
---

{% include base_path %}

## Education

- **Ph.D. Scholar, Centre of Studies in Resources Engineering (CSRE), IIT Bombay** — 2026–Present (CPI: 9.00)
- **M.S. by Research, AI & Data Science, C-MInDS, IIT Bombay** — 2023–2025 (Completed; CPI: 9.31)
- **B.Tech., Mechanical Engineering, MNNIT Allahabad** — 2018–2022 (CPI: 9.10)
- **ISC, Science (PCM) & Languages, De Paul School** — 2015–2017 (98.00%)
- **ICSE, Science (PCM) & Languages, De Paul School** — 2013–2015 (93.80%)

## Work Experience

### Senior AI Data Scientist — Motilal Oswal Financial Services Ltd. (MOFSL)

**Nov 2025–Present**

- Work within the AI Research Team on applied and foundational AI for the Indian context.
- Research time-series and tabular foundation models for financial data.
- Develop Indic TTS/ASR tokenization and production-grade lip-sync systems.
- Develop research aimed at top-tier AI and machine-learning venues.

Project details and results remain high-level because MOFSL work is proprietary.

## Research Internships

- **MOFSL (Sep–Oct 2025):** Evaluated lip-sync and Gaussian-Splatting approaches for high-fidelity synchronization and 3D avatars.
- **Vehant Technologies, Vehant Fellow Track (Sep–Nov 2025):** Researched Pedestrian Attribute Recognition using hyperbolic, graph-based, correlation-aware, and vision-language methods.
- **Sony Research India (May–Jul 2025):** Developed a 3D lip-sync pipeline using Gaussian Splatting and controllable 3D avatars.
- **Clinical AI Assistance (May–Jul 2024):** Fine-tuned LLMs with LoRA and developed a multimodal medical QA system.
- **Reliance Industries Ltd. (Aug 2022–Jul 2023):** Worked as a Graduate Engineer Trainee on predictive maintenance and operational analytics.

## Coursework

**Current (Autumn 2026):** Optimization in Machine Learning; Principles of Satellite Image Processing; Seminar.

**Completed ML/DL coursework:** Foundations of Machine Learning; Advanced Topics in Deep Learning; Medical Image Computing; Algorithms and Complexity; Machine Learning for Remote Sensing II; Statistical Signal Analysis; Image Processing; Optimisation.

## Publications

{% for work in site.data.research.published %}
- **{{ work.title }}.** {{ work.venue }}. {% for link in work.links %}[{{ link.label }}]({{ link.url }}){% unless forloop.last %} · {% endunless %}{% endfor %}
{% endfor %}

### Ongoing Research

{% for work in site.data.research.ongoing %}
- **{{ work.title }}.** {{ work.summary }}
{% endfor %}

## Awards & Honors

- **Award for Excellence in Research**, M.S. by Research, C-MInDS, IIT Bombay — August 22, 2026
- Top 1 percentile — JEE Main 2018
- Top 1 percentile — GATE 2022 (ME & XE)

## Teaching

Teaching Assistant, IIT Bombay:

- **e-PGD: Introduction to Python Programming** — Jan 2025–Present
- **DS 303: Introduction to Machine Learning** — Jul 2024–Present

Student Mentor, MNNIT Allahabad — Jul 2021–May 2022. Mentored more than 20 first-year students and acted as a liaison between students and faculty.

## Professional Service

Reviewer or program committee member for AAAI, AISTATS, ICVGIP, the NeurIPS Position Paper Track, and the International Journal of Computer Vision.

## Skills

Python, C++, PyTorch, TensorFlow, scikit-learn, OpenCV, Hugging Face, Gaussian Splatting, Indic NLP, financial time-series modeling, and production ML systems.
