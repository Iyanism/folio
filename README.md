# Folio

**Folio** is a Medium-style publishing platform built with Django — a clean, distraction-free home for thinkers, creators, storytellers, and lifelong learners. Write and publish stories, discover ideas across tags, follow authors whose work resonates with you, and join the conversation through likes, comments, and replies.

Whether it's a quick reflective piece, a deep technical tutorial, or an ongoing narrative, Folio gives your writing a quiet place to live and a community to reach.

---

## Features

- **Email-based auth & onboarding** — Sign up with your email, then a quick two-step onboarding: claim a unique username, then optionally add a display name, bio, and gender (skippable).
- **Distraction-free editor** — A focus-mode writing page with a Markdown toolbar (bold, italic, headings, quotes, lists, links, code), live word count, auto-computed read time, tag selection, and cover image support.
- **Discovery feed** — The home page surfaces an *Editor's Pick* (most-liked story), a *Most read this week* trending list, and a main feed with **For you**, **Latest**, and **Following** tabs — plus tag filtering and full-text search across titles, bodies, tags, and authors.
- **Social features** — Follow/unfollow authors, like posts *and* comments, and reply in one-level threaded discussions.
- **Bookmarks** — Save stories for later with a dedicated bookmarks page that reuses the same feed, tag, and search filters.
- **Profiles** — A personal profile listing everything you've published, with an edit page featuring a live preview card.
- **Django admin** — Full CRUD over all models at `/admin/`.
- **Seed data** — A management command that fills the site with realistic demo authors, tags, posts, likes, and comments for local exploration.

---

## 🛠️ Tech Stack

| Layer     | Choice                           |
| --------- | -------------------------------- |
| Language  | Python 3.14                      |
| Framework | Django 6.1.2                     |
| Database  | SQLite                           |
| Tooling   | [uv](https://docs.astral.sh/uv/) |
| Frontend  | HTML / CSS (vanilla JS)          |

---

## 🚀 Getting Started

### Requirements

- **Python** `>= 3.14` (see `.python-version`)
- **[uv](https://docs.astral.sh/uv/)** — the project and its dependencies are managed entirely with uv

### 1. Clone the repository

```bash
git clone https://github.com/Iyanism/folio.git
cd folio
```

### 2. Sync dependencies

```bash
uv sync
```

This creates a virtual environment and installs Django (plus dev tools like `ruff` and `django-stubs`).

### 3. Run migrations

```bash
uv run manage.py migrate
```

### 4. Create a superuser

```bash
uv run manage.py createsuperuser
```

> **Note:** Folio uses a custom user model where the **email address is the login identifier** (not a username). The prompts will ask for an email, password, and name — use your email to log in everywhere, including the admin panel.

### 5. Seed demo data *(optional)*

```bash
uv run manage.py seed_posts
```

This populates the site with four fictional authors, eight tags, and a dozen hand-written posts complete with likes and comments — handy for exploring the feed without writing anything first. Add `--wipe` to clear previously seeded posts before reseeding:

```bash
uv run manage.py seed_posts --wipe
```

### 6. Launch the development server

```bash
uv run manage.py runserver
```

Visit **http://127.0.0.1:8000/** to browse the feed, and **http://127.0.0.1:8000/admin/** to manage content through the Django admin.

---

## 📱 How to Use

1. **Sign up** at `/accounts/signup/` with your email and a password.
2. **Onboarding** — Step 1: claim a unique username. Step 2: optionally add a display name, bio, and gender (or skip straight to your feed).
3. **Write a story** — Hit the editor, give your piece a title and subtitle, write in plain text/Markdown, pick tags, and drop in a cover image URL. Read time is calculated automatically.
4. **Discover** — The home feed lets you browse the featured pick, trending stories, and tabs for *For you*, *Latest*, and *Following*. Filter by tag or search for anything.
5. **Engage** — Like posts and comments, leave responses (with inline replies), bookmark stories to revisit later, and follow authors whose work you enjoy.
6. **Manage your profile** — View everything you've published on your profile page, and tweak your identity anytime from the edit screen with a live preview.

---

## 🤝 A Personal Note

Django is something I'm actively learning. There are probably mistakes in here — rough edges, things done in a way a more experienced developer would do differently. But it feels good making it, and that's what counts.

---

## 📄 License

This project is under active development. License details will be specified upon public release.
