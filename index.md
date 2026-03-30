---
layout: default
title: Home
---

# Welcome to allclaws

A comprehensive multi-agent AI framework bringing together different agent implementations under a unified testing and benchmarking system.

## Quick Links

- 📖 [Documentation](README.md)
- 📝 [Blog](blog/)
- 🧪 [Test Framework](test_framework/)
- 🏗️ [Architecture](architecture/)
- 💻 [GitHub Repository](https://github.com/dz3ai/allclaws)

## Latest Blog Posts

{% assign posts = site.posts | sort: 'date' | reverse | limit: 3 %}

{% if posts.size > 0 %}
  <div class="recent-posts">
    {% for post in posts %}
      <article class="post-summary">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
        <p class="post-meta">{{ post.date | date: "%B %d, %Y" }}</p>
        {% if post.excerpt %}
          <p>{{ post.excerpt | strip_html | truncate: 150 }}</p>
        {% endif %}
      </article>
    {% endfor %}
  </div>

  <p><a href="{{ site.baseurl }}/blog/">View all posts →</a></p>
{% endif %}

<style>
  .recent-posts {
    margin-top: 2rem;
  }

  .post-summary {
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: #f9f9f9;
    border-radius: 4px;
  }

  .post-summary h3 {
    margin: 0 0 0.5rem 0;
  }

  .post-summary h3 a {
    color: #333;
    text-decoration: none;
  }

  .post-summary h3 a:hover {
    color: #0066cc;
  }

  .post-meta {
    color: #666;
    font-size: 0.85rem;
    margin: 0 0 0.5rem 0;
  }

  .post-summary p {
    margin: 0;
    color: #444;
  }
</style>
