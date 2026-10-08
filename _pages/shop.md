---
layout: page
permalink: /shop/
title: shop
description: Instruments and a few things for the home. Pay here, or in store.
nav: true
nav_order: 2
---

Everything here is also on the shelf in the shop, where you can hear it before
you buy. Online payment is handled by Stripe — card, Apple Pay and Google Pay.

<div class="shop-grid">
  {% for item in site.data.products %}
    <div class="shop-card">
      {% if item.image %}
        <img src="{{ item.image | prepend: '/assets/img/shop/' | relative_url }}" alt="" loading="lazy" />
      {% endif %}
      <h3>{{ item.name }}</h3>
      {% if item.note %}<p class="shop-note">{{ item.note }}</p>{% endif %}
      <p class="shop-desc">{{ item.description }}</p>
      <div class="shop-foot">
        <span class="shop-price">{{ item.price }}</span>
        {% if item.origin %}<span class="shop-origin">{{ item.origin }}</span>{% endif %}
      </div>
      {% if item.checkout_url and item.checkout_url != "" %}
        <a class="shop-buy" href="{{ item.checkout_url }}">Buy</a>
      {% else %}
        <span class="shop-buy shop-buy--disabled">Ask in store</span>
      {% endif %}
    </div>
  {% endfor %}
</div>

## Collection and delivery

<!-- Replace with what you actually offer: collection only, local delivery, postage. -->

_To be confirmed._

## Returns

<!--
  Required in the UK and EU for distance selling: customers generally have 14
  days to change their mind on an online order. State the policy plainly here
  before taking the first payment.
-->

_To be confirmed._
