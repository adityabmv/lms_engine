from django.db import models

from ...auth.permissions import ModelPermissionsMixin
from ...utils.models import TimestampMixin
from . import Section


class ItemTypeChoices(models.TextChoices):
    ARTICLE = "article", "Article"
    ASSESSMENT = "assessment", "Assessment"
    VIDEO = "video", "Video"

class SectionItemInfo(models.Model):
    section = models.ForeignKey(
        "Section",
        on_delete=models.CASCADE,
        related_name="section_items",
        help_text="The section this item belongs to.",
    )
    sequence = models.PositiveIntegerField(
        help_text="The order of this item within the section."
    )
    item_type = models.CharField(
        choices=ItemTypeChoices.choices,
        max_length=20,
        help_text="The type of this section item (video, article, etc.).",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "sequence"],
                name="unique_section_sequence",
            )
        ]
        ordering = ["sequence"]

    def __str__(self):
        return f"{self.section} - Item Sequence {self.sequence}"


#
# class SectionItem(TimestampMixin, ModelPermissionsMixin, models.Model):
#     section = models.ForeignKey(
#         Section,
#         on_delete=models.CASCADE,
#         related_name="%(class)ss",  # Dynamically generate related_name
#         help_text="The section this item belongs to.",
#     )
#     item_type = models.CharField(choices=ItemTypeChoices.choices, max_length=20)
#     sequence = models.PositiveIntegerField(
#         help_text="The order of this item within the section."
#     )
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["section", "sequence"], name="%(class)s_sequence_in_section"
#             )
#         ]
#         ordering = ["sequence"]
#         abstract = True
#
#     def __str__(self):
#         return f"{self.section} - Item Sequence {self.sequence}"
#
#     def __getattr__(self, name):
#         """
#         Delegate permission checks to the related section object.
#         """
#         if name.endswith("_has_access"):
#             return getattr(self.section, name)
#         raise AttributeError(
#             f"'{type(self).__name__}' object has no attribute '{name}'"
#         )

class SectionItemBase(TimestampMixin, ModelPermissionsMixin, models.Model):
    section_item_info = None  # Placeholder for the associated SectionItemInfo
    item_type = 'BaseItem'

    class Meta:
        abstract = True

    def __init__(self, *args, section=None, sequence=None, **kwargs):
        """
        Override the default __init__ method to handle pseudo-parameters.
        """
        super().__init__(*args, **kwargs)

        # Ensure that section and sequence are provided during instantiation
        if section is None or sequence is None:
            raise ValueError("'section' and 'sequence' must be provided.")

        # Ensure the item type is defined in the concrete class
        if not hasattr(self, "item_type"):
            raise ValueError("Concrete classes must define 'item_type'.")

        # Create or update the SectionItemInfo
        self.section_item_info, _ = SectionItemInfo.objects.update_or_create(
            section=section,
            sequence=sequence,
            defaults={"item_type": self.item_type},
        )

    @property
    def section(self):
        """
        Access the section from the associated SectionItemInfo.
        """
        return self.section_item_info.section if self.section_item_info else None

    @property
    def sequence(self):
        """
        Access the sequence from the associated SectionItemInfo.
        """
        return self.section_item_info.sequence if self.section_item_info else None
