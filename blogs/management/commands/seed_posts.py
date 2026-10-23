import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserProfile
from blogs.models import Comment, Like, Post, Tag

User = get_user_model()

AUTHORS = [
    ("maya.sen@folio.test", "Maya Sen", "maya"),
    ("theo.araki@folio.test", "Theo Araki", "theo"),
    ("ines.duarte@folio.test", "Inés Duarte", "ines"),
    ("jonah.k@folio.test", "Jonah Kim", "jonah"),
]

TAGS = [
    "Science",
    "Programming",
    "Travel",
    "Daily life",
    "People",
    "News",
    "The case against",
    "Technology",
]

POSTS = [
    # (title, subtitle, tag, cover_url, likes_target, comments_target)
    (
        "The quiet search for a second Earth has entered its most interesting chapter",
        "New instruments are turning a distant flicker into a map of possibility.",
        "Science",
        "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1200&q=80",
        42,
        3,
    ),
    (
        "Why your app feels slow (and what concurrency actually fixes)",
        "A practical tour of the three kinds of latency that dominate user perception.",
        "Programming",
        "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&q=80",
        31,
        2,
    ),
    (
        "A practical guide to having better hard conversations",
        "A short field guide to opening, holding, and closing the ones that matter.",
        "People",
        "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1200&q=80",
        58,
        5,
    ),
    (
        "The long way home: a night train across the Balkans",
        "Eighteen hours, four borders, one sleeper carriage.",
        "Travel",
        "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=1200&q=80",
        27,
        1,
    ),
    (
        "The case against productivity systems",
        "Every productivity system promises the same thing. It won't.",
        "The case against",
        "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200&q=80",
        45,
        4,
    ),
    (
        "A field guide to slow travel",
        "The best trips aren't the longest. They're the ones where you stop counting.",
        "Travel",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80",
        19,
        0,
    ),
    (
        "The 20-minute reset for noisy days",
        "A small ritual for the middle of a day that has gone sideways.",
        "Daily life",
        "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1200&q=80",
        22,
        1,
    ),
    (
        "What concurrency actually means (and what it doesn't)",
        "The word gets thrown around as if it were a feature.",
        "Technology",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&q=80",
        36,
        2,
    ),
    (
        "A better way to take notes while you read",
        "Margin notes, index cards, and reading with a pen in your hand.",
        "Daily life",
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&q=80",
        14,
        0,
    ),
    (
        "How to ask a question that opens a room",
        "The difference between a closing and opening question is smaller than you think.",
        "People",
        "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?w=1200&q=80",
        29,
        2,
    ),
    (
        "The new etiquette of AI",
        "We're inventing the social rules for a technology that has none.",
        "Technology",
        "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&q=80",
        51,
        3,
    ),
    (
        "Small budgets, long horizons",
        "The best work rarely comes from the biggest budget.",
        "The case against",
        "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&q=80",
        17,
        1,
    ),
]
FILLER = (
    "There is a particular kind of attention that only arrives when you stop trying to be efficient. "
    "It shows up in the margins of a notebook, on the third hour of a train ride, in the pause after a question you didn't expect. "
) * 6


class Command(BaseCommand):
    help = "Seed the database with sample authors, tags, posts, likes, and comments."

    def add_arguments(self, parser):
        parser.add_argument("--wipe", action="store_true")

    def handle(self, *args, **options):
        random.seed(42)

        if options["wipe"]:
            Post.objects.filter(author__email__endswith="@folio.test").delete()
            self.stdout.write(self.style.WARNING("Wiped previous seed posts."))

        # ── Authors ────────────────────────────────────────────
        authors = []
        for email, display_name, username in AUTHORS:
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.set_unusable_password()
                user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.display_name = display_name

            # Guard against unique username collisions
            final_username = username
            if (
                UserProfile.objects.filter(username=final_username)
                .exclude(pk=profile.pk)
                .exists()
            ):
                final_username = f"{username}-{user.pk}"
            profile.username = final_username
            profile.save()

            authors.append(user)

        self.stdout.write(self.style.SUCCESS(f"Authors ready: {len(authors)}"))

        # ── Tags ───────────────────────────────────────────────
        tag_map = {name: Tag.objects.get_or_create(name=name)[0] for name in TAGS}
        self.stdout.write(self.style.SUCCESS(f"Tags ready: {len(tag_map)}"))

        # ── Posts ──────────────────────────────────────────────
        created_posts = []
        now = timezone.now()

        for idx, (
            title,
            subtitle,
            tag_name,
            cover_url,
            likes_target,
            comments_target,
        ) in enumerate(POSTS):
            post, created = Post.objects.get_or_create(
                title=title,
                defaults={
                    "subtitle": subtitle,
                    "body": FILLER,
                    "cover_url": cover_url,
                    "author": authors[idx % len(authors)],
                },
            )
            if not created:
                created_posts.append(post)
                continue

            Post.objects.filter(pk=post.pk).update(
                publish_date=now - timedelta(days=idx * 2, hours=idx)
            )
            post.refresh_from_db()

            post.tags.add(tag_map[tag_name])
            created_posts.append(post)

            for i in range(likes_target):
                liker = authors[(idx + i) % len(authors)]
                Like.objects.get_or_create(user=liker, post=post)

            for i in range(comments_target):
                commenter = authors[(idx + i + 1) % len(authors)]
                Comment.objects.create(
                    body=random.choice(
                        [
                            "This is exactly what I needed to read today.",
                            "The distinction you draw here is the whole argument.",
                            "Saved. Re-reading on the weekend.",
                            "I keep coming back to this paragraph.",
                            "Quietly one of the best pieces on the site.",
                        ]
                    ),
                    user=commenter,
                    post=post,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(created_posts)} posts with likes and comments."
            )
        )
