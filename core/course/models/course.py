from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

from ...auth.permissions import ModelPermissionsMixin
from ...utils.models import TimestampMixin
from ...user.models import User, Roles
from ..constants import COURSE_NAME_MAX_LEN, COURSE_DESCRIPTION_MAX_LEN


# Visibility choices for courses
class VisibilityChoices(models.TextChoices):
    PUBLIC = "public", "Public"       # Publicly visible courses
    PRIVATE = "private", "Private"   # Only visible within certain institutions
    UNLISTED = "unlisted", "Unlisted" # Hidden courses that require a direct link


# Custom manager for the Course model
class CourseManager(models.Manager):
    """
    Provides custom query methods to retrieve courses based on the user's role and access permissions.
    """

    def accessible_by(self, user: User):
        """
        Returns courses accessible by the given user, depending on their role.

        Args:
            user (User): The user requesting course access.

        Returns:
            QuerySet: A filtered queryset of courses accessible to the user.
        """
        if user.role in [Roles.SUPERADMIN, Roles.ADMIN]:
            # Superadmins and admins have access to all courses
            return self.all()

        elif user.role == Roles.MODERATOR:
            # Moderators can access courses associated with their institutions
            return self.filter(
                institution_id__in=user.institutions.values_list("id", flat=True)
            )

        elif user.role == Roles.INSTRUCTOR:
            # Instructors can access:
            # - Public courses
            # - Private courses in their institutions
            # - Courses where they are explicitly listed as instructors
            user_institutions = user.institutions.values_list("id", flat=True)
            return self.filter(
                Q(visibility=VisibilityChoices.PUBLIC)
                | Q(
                    institutions__id__in=user_institutions,
                    visibility=VisibilityChoices.PRIVATE,
                )
                | Q(instructors__contains=user)
            )

        elif user.role == Roles.STAFF:
            # Staff members can access:
            # - Public courses
            # - Private courses in their institutions
            # - Courses they are directly assigned to as staff
            user_institutions = user.institutions.values_list("id", flat=True)
            return self.filter(
                Q(visibility=VisibilityChoices.PUBLIC)
                | Q(
                    institutions__id__in=user_institutions,
                    visibility=VisibilityChoices.PRIVATE,
                )
            ).union(
                user.personnel_courses.all()  # type: ignore
            )

        elif user.role == Roles.STUDENT:
            # Students can access:
            # - Public courses
            # - Private courses in their institutions
            # - Courses they are enrolled in
            user_institutions = user.institutions.values_list("id", flat=True)
            return self.filter(
                Q(visibility=VisibilityChoices.PUBLIC)
                | Q(
                    institutions__id__in=user_institutions,
                    visibility=VisibilityChoices.PRIVATE,
                )
            ).union(user.courses.all())


# Main Course model
class Course(TimestampMixin, ModelPermissionsMixin, models.Model):
    """
    Represents a course in the system.

    Attributes:
        name (str): The name of the course.
        description (str): A brief description of the course.
        visibility (VisibilityChoices): Defines the visibility of the course.
        institutions (ManyToMany): Institutions offering the course.
        instructors (ManyToMany): Instructors teaching the course.
    """
    name = models.CharField(max_length=COURSE_NAME_MAX_LEN)
    description = models.TextField(max_length=COURSE_DESCRIPTION_MAX_LEN)
    visibility = models.CharField(
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLIC,
        help_text="Set the visibility of the course.",
        max_length=21,
    )
    institutions = models.ManyToManyField(
        "institution.Institution", related_name="courses"
    )
    instructors = models.ManyToManyField(
        "user.User", through="CourseInstructor", related_name="instructor_courses"
    )

    # Assign the custom manager
    objects: CourseManager = CourseManager()

    def __str__(self):
        return self.name

    # Access control methods
    def student_has_access(self, user: User):
        """
        Determines if a student has access to this course.
        """
        is_read_allowed = (
            user.courses.filter(course=self).exists()  # Enrolled courses
            or self.visibility == VisibilityChoices.PUBLIC
            or (
                self.visibility == VisibilityChoices.PRIVATE
                and self.institutions.intersection(user.institutions).exists()
            )  # Institution's private courses
        )
        return (is_read_allowed, False, False)

    def instructor_has_access(self, user: User):
        """
        Determines if an instructor has access to this course.
        """
        is_course_instructor = self.instructors.filter(pk=user.pk).exists()
        is_read_allowed = (
            is_course_instructor
            or self.visibility == VisibilityChoices.PUBLIC
            or (
                self.visibility == VisibilityChoices.PRIVATE
                and self.institutions.intersection(user.institutions).exists()
            )
        )
        return (is_read_allowed, is_course_instructor, False)

    def staff_has_access(self, user: User):
        """
        Determines if a staff member has access to this course.
        """
        is_course_staff = user.personnel_courses.filter(  # type: ignore
            pk=self.pk
        ).exists()
        is_read_allowed = (
            is_course_staff
            or self.visibility == VisibilityChoices.PUBLIC
            or (
                self.visibility == VisibilityChoices.PRIVATE
                and self.institutions.intersection(user.institutions).exists()
            )
        )
        return (is_read_allowed, False, False)

    def moderator_has_access(self, user: User):
        """
        Determines if a moderator has access to this course.
        """
        has_access = self.institutions.intersection(user.institutions).exists()
        return (has_access, has_access, False)

    def admin_has_access(self, user: User):
        """
        Determines if an admin has access to this course.
        """
        return (True, True, False)


# Through table for instructor-course relationships
class CourseInstructor(models.Model):
    """
    Represents the relationship between a course and its instructors.

    Attributes:
        course (ForeignKey): The course the instructor is assigned to.
        instructor (ForeignKey): The instructor assigned to the course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "instructor"], name="unique_course_instructor"
            )
        ]

    def clean(self, *args, **kwargs):
        """
        Ensures that only users with the 'instructor' role can be assigned as instructors.
        """
        if self.instructor.role != "instructor":
            raise ValidationError(
                "Only users with the 'instructor' role can be added to the instructors."
            )
        super().clean(*args, **kwargs)

    def __str__(self):
        return f"{self.instructor} - {self.course}"
