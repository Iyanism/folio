from django import forms

from blogs.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "subtitle", "body", "tags", "cover_url")
        widgets = {
            "title": forms.Textarea(
                attrs={
                    "class": "editor-field editor-title",
                    "rows": 2,
                    "maxlength": 140,
                    "placeholder": "Title",
                    "required": True,
                    "autocomplete": "off",
                }
            ),
            "subtitle": forms.Textarea(
                attrs={
                    "class": "editor-field editor-subtitle",
                    "rows": 2,
                    "maxlength": 240,
                    "placeholder": "A subtitle: one or two sentences that tell readers what to expect",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "editor-field editor-body",
                    "rows": 14,
                    "placeholder": "Tell the story. Start with what you figured out, or the question you could not stop thinking about.",
                    "required": True,
                }
            ),
            "tags": forms.CheckboxSelectMultiple(),
            "cover_url": forms.URLInput(attrs={"placeholder": "https://…"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body", "parent")
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add to the discussion",
                    "required": True,
                }
            )
        }
