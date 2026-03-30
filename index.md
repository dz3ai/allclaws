---
layout: default
title: Home
---

<div class="hero">
  <div class="container">
    <h1>{{ site.title }}</h1>
    <p>{{ site.description }}</p>
    <p style="margin-top: 2rem;">
      <a href="{{ '/blog/' | relative_url }}" class="btn">Read the Blog</a>
      <a href="https://github.com/{{ site.github.username }}/{{ site.github.repository }}" class="btn btn-secondary" style="margin-left: 1rem;">View on GitHub</a>
    </p>
  </div>
</div>

<div class="container">
  <h2 style="text-align: center; margin-bottom: 2rem;">Latest Posts</h2>

  {% assign posts = site.posts | sort: 'date' | reverse | limit: 3 %}

  {% if posts.size > 0 %}
    {% for post in posts %}
      <article class="blog-post">
        <h2 class="blog-post-title">
          <a href="{{ post.url }}">{{ post.title }}</a>
        </h2>
        <div class="blog-post-meta">
          <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
          {% if post.author %} • {{ post.author }}{% endif %}
        </div>
        {% if post.excerpt %}
        <div class="blog-post-excerpt">
          {{ post.excerpt | strip_html | truncate: 200 }}
        </div>
        {% endif %}
        {% if post.tags %}
        <div class="blog-post-tags">
          {% for tag in post.tags limit: 3 %}
            <span class="tag">{{ tag }}</span>
          {% endfor %}
        </div>
        {% endif %}
      </article>
    {% endfor %}

    <p style="text-align: center; margin-top: 2rem;">
      <a href="{{ '/blog/' | relative_url }}" class="btn btn-secondary">View All Posts →</a>
    </p>
  {% else %}
    <p style="text-align: center; color: var(--color-text-light);">No posts yet. Check back soon!</p>
  {% endif %}
</div>
