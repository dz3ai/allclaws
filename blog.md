---
layout: default
title: Blog
permalink: /blog/
---

# Blog

Thoughts, tutorials, and updates from the allclaws project.

{% assign posts = site.posts | sort: 'date' | reverse %}

{% if posts.size == 0 %}
  <p>No posts yet. Check back soon!</p>
{% else %}
  <div class="posts-list">
    {% for post in posts %}
      <article class="post-summary">
        <header>
          <h2>
            <a href="{{ post.url }}">{{ post.title }}</a>
          </h2>
          <p class="post-meta">
            <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
            {% if post.author %} • {{ post.author }}{% endif %}
            {% if post.categories %} • {{ post.categories | array_to_sentence_string }}{% endif %}
          </p>
        </header>

        {% if post.excerpt %}
          <div class="post-excerpt">
            {{ post.excerpt }}
            <p><a href="{{ post.url }}">Read more →</a></p>
          </div>
        {% endif %}

        {% if post.tags %}
          <p class="post-tags">Tags: {{ post.tags | array_to_sentence_string }}</p>
        {% endif %}
      </article>
    {% endfor %}
  </div>
{% endif %}

<style>
  .posts-list {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .post-summary {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #e0e0e0;
  }

  .post-summary:last-child {
    border-bottom: none;
  }

  .post-summary h2 {
    margin: 0 0 0.5rem 0;
  }

  .post-summary h2 a {
    color: #333;
    text-decoration: none;
  }

  .post-summary h2 a:hover {
    color: #0066cc;
  }

  .post-meta {
    color: #666;
    font-size: 0.9rem;
    margin: 0 0 1rem 0;
  }

  .post-excerpt {
    color: #444;
    line-height: 1.6;
  }

  .post-excerpt a {
    color: #0066cc;
    text-decoration: none;
  }

  .post-excerpt a:hover {
    text-decoration: underline;
  }

  .post-tags {
    color: #666;
    font-size: 0.9rem;
    margin: 1rem 0 0 0;
  }
</style>
