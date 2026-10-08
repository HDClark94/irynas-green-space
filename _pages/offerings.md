---
layout: page
permalink: /offerings/
title: offerings
description: Four things under one roof, from the same idea.
nav: true
nav_order: 1
---

<div class="offerings-grid">
  {% assign sorted = site.offerings | sort: 'order' %}
  {% for item in sorted %}
    <a class="offering-card" href="{{ item.url | relative_url }}">
      {% if item.image %}
        <img src="{{ item.image | prepend: '/assets/img/offerings/' | relative_url }}" alt="" loading="lazy" />
      {% endif %}
      <h3>{{ item.title }}</h3>
      <p>{{ item.description }}</p>
      {% if item.status %}<span class="offering-status">{{ item.status }}</span>{% endif %}
    </a>
  {% endfor %}
</div>
