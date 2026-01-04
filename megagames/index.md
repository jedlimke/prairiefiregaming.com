---
layout: page
title: Megagames
permalink: /megagames/
---

<h1>Megagames</h1>

<!-- Featured: Den of Wolves megagame page -->
<article class="post-summary post-summary--with-image post-summary--featured">
  <a href="{{ site.baseurl }}/megagames/den-of-wolves-2026/" class="post-summary-link">
    <div class="post-summary-image">
      <img src="/assets/megagames/den-of-wolves-hero.jpg" alt="Den of Wolves: Infinite Domain" loading="eager">
    </div>
    <div class="post-summary-content">
      <header class="post-header">
        <h2 class="fancy-text">Den of Wolves: Infinite Domain</h2>
        <p class="post-meta">
          <time datetime="2026-03-07" style="font-size: 1.5em;">Coming <strong>March 7, 2026</strong></time>
        </p>
      </header>
      <p>60 players! 6 hours! 100% fun! Inspired by the pilot of <em>Battlestar Galactica</em>, <strong>Den of Wolves</strong> is a cooperative megagame that combines elements of board games and diplomacy. Players cooperate to allocate resources while fending off waves of attacks from the vile "wolves". Beware! These wolves are tricky, and a traitor may roam amongst us.</p>
    </div>
  </a>
</article>

<!-- Past events from posts -->
{% assign result_posts = site.posts %}

{% for post in result_posts %}
  <article class="post-summary{% if post.image %} post-summary--with-image{% endif %}">
	<a href="{{ post.url | relative_url }}" class="post-summary-link">
		{% if post.image %}
		  <div class="post-summary-image">
			<img src="{{ post.image | relative_url }}" alt="{{ post.title | escape }}" loading="lazy">
		  </div>
		{% endif %}
		<div class="post-summary-content">
			<header class="post-header">
				<h2>{{ post.title }}</h2>
				<p class="post-meta">
					<time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
				</p>
			</header>
			{% if post.excerpt %}
			  <p>{{ post.excerpt | strip_html }}</p>
			{% endif %}
		</div>
	</a>
  </article>
{% endfor %}

{% if result_posts.size == 0 %}
  <p>No past events yet.</p>
{% endif %}
