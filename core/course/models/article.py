from django.db import models

from . import SectionItemBase, ItemTypeChoices
from ..constants import ARTICLE_MAX_LENGTH


class Article(SectionItemBase):
    item_type = ItemTypeChoices.ARTICLE

    content = models.TextField(max_length=ARTICLE_MAX_LENGTH)

    def admin_has_access(self, user: "User"):
        return True, True, True
