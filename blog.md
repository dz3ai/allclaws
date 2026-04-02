---
layout: default
title: Blog
permalink: /blog/
---

<div class="container">
  <div style="text-align: center; margin-bottom: 3rem;">
    <h1>Blog</h1>
    <p style="color: var(--color-text-light); font-size: 1.1rem;">Thoughts, tutorials, and updates from the {{ site.title }} project.</p>
  </div>

  {% assign posts = site.posts | sort: 'date' | reverse %}

  {% if posts.size == 0 %}
    <div style="text-align: center; padding: 3rem 0;">
      <p style="color: var(--color-text-light); font-size: 1.1rem;">No posts yet. Check back soon!</p>
    </div>
  {% else %}
    {% for post in posts %}
      <article class="blog-post">
        <h2 class="blog-post-title">
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        </h2>
        <div class="blog-post-meta">
          <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
          {% if post.author %} • {{ post.author }}{% endif %}
          {% if post.categories %} • {{ post.categories | array_to_sentence_string }}{% endif %}
        </div>
        {% if post.excerpt %}
        <div class="blog-post-excerpt">
          {{ post.excerpt }}
        </div>
        {% endif %}
        {% if post.tags %}
        <div class="blog-post-tags">
          {% for tag in post.tags %}
            <span class="tag">{{ tag }}</span>
          {% endfor %}
        </div>
        {% endif %}
      </article>
    {% endfor %}

    <!-- Pagination -->
    {% if paginator.total_pages > 1 %}
    <div style="text-align: center; margin-top: 3rem;">
      {% if paginator.previous_page %}
        <a href="{{ paginator.previous_page_path }}" class="btn btn-secondary">← Previous</a>
      {% endif %}

      <span style="margin: 0 1rem;">
        Page {{ paginator.page }} of {{ paginator.total_pages }}
      </span>

      {% if paginator.next_page %}
        <a href="{{ paginator.next_page_path }}" class="btn btn-secondary">Next →</a>
      {% endif %}
    </div>
    {% endif %}

    <!-- View All Posts link (when not on first page) -->
    {% if page.url != '/blog/' %}
    <div style="text-align: center; margin-top: 2rem;">
      <a href="/blog/" class="btn btn-secondary">View All Posts →</a>
    </div>
    {% endif %}
  {% endif %}
</div>
