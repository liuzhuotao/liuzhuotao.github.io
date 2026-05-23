---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: '6rem'

sections:
  - block: group-intro
    content:
      title: About InspiringGroup
      text: >-
        The InspiringGroup is a dynamic research group led by [Prof. Zhuotao
        Liu](/authors/liuzhuotao/). We build trustworthy AI systems for
        real-world networked and distributed environments. Our research spans
        networking, systems, security, and applied cryptography, with a focus on
        deployable AI, robust learning-based systems, and privacy-preserving
        collaboration.
    design:
      css_class: hbx-bg-gradient
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: liuzhuotao
      text: ''
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Download CV
        url: uploads/resume.pdf
      headings:
        about: 'Biography'
        education: ''
        interests: ''
    design:
      # Apply a gradient background
      css_class: hbx-bg-gradient
      # Avatar customization
      avatar:
        size: xl # Options: small (150px), medium (200px, default), large (320px), xl (400px), xxl (500px)
        shape: circle # Options: circle (default), square, rounded
  - block: research-areas
    content:
      title: ''
      subtitle: ''
      text: ''
      side_title: Research Topic
      source_folder: research-topics
    design:
      layout: taxonomy-grid
      spacing:
        padding: [0, 0, 0, 0]
  - block: collection
    id: news
    content:
      title: Recent News
      subtitle: ''
      text: ''
      manual_items:
        - title: 'PhD/RA Opening: Network Security & Privacy'
          summary: 'We are actively recruiting self-motivated PhD students and research assistants. Prior background in systems, security, or machine learning is a plus.'
          url: '/join'
          date: 'Apr 2026'
          badge: 'Hiring'
        - title: 'We welcome collaboration from academia and industry'
          summary: 'If your team is interested in joint projects on secure networking, privacy-preserving AI, or Web3 infrastructure, please feel free to reach out.'
          # url: '/#contact'
          date: 'Apr 2026'
          badge: 'Pinned'
      # Page type to display. E.g. post, talk, publication...
      page_type: news
      # Choose how many pages you would like to display (0 = all pages)
      count: 5
      # Filter on criteria
      filters:
        author: ''
        category: ''
        tag: ''
        exclude_featured: false
        exclude_future: false
        exclude_past: false
        publication_type: ''
      # Choose how many pages you would like to offset by
      offset: 0
      # Page order: descending (desc) or ascending (asc) date.
      order: desc
    design:
      # Choose a layout view
      view: card
      # Reduce spacing
      spacing:
        padding: [0, 0, 0, 0]
---
