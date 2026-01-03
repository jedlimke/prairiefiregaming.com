---
layout: page
title: Events
permalink: /events/
---

<h1>Events</h1>

<!-- Featured: Den of Wolves megagame page -->
<article class="post-summary">
  <header class="post-header">
    <h2><a class="fancy-text" href="{{ site.baseurl }}/events/den-of-wolves-2026/">Den of Wolves: Infinite Domain</a></h2>
    <p class="post-meta">
      <time datetime="2026-03-07" style="font-size: 1.5em;">Coming <strong>March 7, 2026</strong></time>
    </p>
  </header>
  <p>60 players! 6 hours! 100% fun! Inspired by the pilot of <em>Battlestar Galactica</em>, <strong>Den of Wolves</strong> is a cooperative megagame that combines elements of board games and diplomacy. Players cooperate to allocate resources while fending off waves of attacks from the vile "wolves". Beware! These wolves are tricky, and a traitor may roam amongst us.</p>
</article>

<!-- Past events from posts -->
{% assign result_posts = site.posts %}

{% for post in result_posts %}
  <article class="post-summary">
	<header class="post-header">
		<h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
		<p class="post-meta">
			<time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
		</p>
	</header>
    {% if post.excerpt %}
      <p>{{ post.excerpt | strip_html }}</p>
    {% endif %}
  </article>
{% endfor %}

{% if result_posts.size == 0 %}
  <p>No past events yet.</p>
{% endif %}
