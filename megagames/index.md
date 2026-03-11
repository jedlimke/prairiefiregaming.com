---
layout: page
title: Megagames
permalink: /megagames/
---

<h1>Megagames</h1>

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
