---
layout: page
permalink: /publications/
title: publications
description: Grouped by status, newest first. Also on Google Scholar.
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->
<!-- Sections come from the pubgroup field of each entry in _bibliography/papers.bib -->

<style>
  .publications h2.pub-group {
    color: var(--global-text-color);
    font-size: 1.5rem;
    font-weight: 400;
    border-top: 1px solid var(--global-divider-color);
    padding-top: 1rem;
    margin-top: 2.5rem;
  }
  .publications h2.pub-group:first-of-type { margin-top: 1rem; }
</style>

{% include bib_search.liquid %}

<div class="publications">

<h2 class="pub-group">Peer-Reviewed Publications</h2>
{% bibliography --group_by none --query @*[pubgroup=reviewed]* %}

<h2 class="pub-group">Under Review</h2>
{% bibliography --group_by none --query @*[pubgroup=underreview]* %}

<h2 class="pub-group">Preprints</h2>
{% bibliography --group_by none --query @*[pubgroup=preprint]* %}

</div>
