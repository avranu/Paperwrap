"""




----------------------------------------------------------------------------

   METADATA:

       File:    base.py
        Project: paperap
       Created: 2025-03-04
        Version: 0.0.1
       Author:  Jess Mann
       Email:   jess@jmann.me
        Copyright (c) 2025 Jess Mann

----------------------------------------------------------------------------

   LAST MODIFIED:

       2025-03-04     By Jess Mann

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar, Generic, Self, TYPE_CHECKING
from typing_extensions import TypeVar

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from yarl import URL

from paperap.models.abstract.parser import Parser
from paperap.models.abstract.queryset import QuerySet

if TYPE_CHECKING:
    from paperap.resources.base import PaperlessResource

_Self = TypeVar("_Self", bound="PaperlessModel")


class PaperlessModel(BaseModel, ABC):
    """
    Base model for all Paperless-ngx API objects.

    Provides automatic serialization, deserialization, and API interactions
    with minimal configuration needed.

    Examples:
        from paperap.models.abstract.model import PaperlessModel
        class Document(PaperlessModel):
            filename: str
            contents : bytes

            class Meta:
                api_endpoint: = URL("http://localhost:8000/api/documents/")
    """

    id: int = Field(description="Unique identifier", default=0)
    created: datetime = Field(description="Creation timestamp", default_factory=datetime.now, alias="created_on")
    updated: datetime = Field(description="Last update timestamp", default_factory=datetime.now, alias="updated_on")

    _meta: "Meta[Self]" = PrivateAttr()

    class Meta(Generic[_Self]):
        # The name of the model.
        # It will default to the classname
        name: str
        # Fields that should not be modified
        read_only_fields: set[str] = {"id", "created", "updated"}
        # the type of parser, which parses api data into appropriate types
        # this will usually not need to be overridden
        parser: type[Parser] = Parser
        resource: "PaperlessResource[_Self]"
        queryset: type[QuerySet[_Self]] = QuerySet

    # Configure Pydantic behavior
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
        json_encoders={
            # Custom JSON encoders for types
            datetime: lambda dt: dt.isoformat().replace("+00:00", "Z")
            if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt).total_seconds() == 0
            else dt.isoformat(),
            Decimal: lambda d: float(d),
        },
    )

    def __init__(self, resource: "PaperlessResource", **data):
        if resource is None:
            raise ValueError("Resource is required for PaperlessModel")
        super().__init__(**data)
        self._meta.resource = resource

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Instantiate _meta
        cls._meta = cls.Meta()

        # Set name defaults
        if not hasattr(cls._meta, "name"):
            cls._meta.name = cls.__name__.lower()

        # Append read_only_fields from all parents to _meta
        read_only_fields = (cls._meta.read_only_fields or set()).copy()
        for base in cls.__bases__:
            if hasattr(base, "_meta") and hasattr(base._meta, "read_only_fields"):
                read_only_fields.update(base._meta.read_only_fields)

        cls._meta.read_only_fields = read_only_fields

    @classmethod
    def from_dict(cls, data: dict[str, Any], resource: "PaperlessResource") -> Self:
        """
        Create a model instance from API response data.

        Args:
            data (dict[str, Any]): dictionary containing the API response data.

        Returns:
            A model instance initialized with the provided data.
        """
        return cls.model_validate({**data, "resource": resource})

    def to_dict(
        self, *, include_read_only: bool = True, exclude_none: bool = True, exclude_unset: bool = True
    ) -> dict[str, Any]:
        """
        Convert the model to a dictionary for API requests.

        Args:
            include_read_only (bool): Whether to include read-only fields.
            exclude_none (bool): Whether to exclude fields with None values.
            exclude_unset (bool): Whether to exclude fields that are not set.

        Returns:
            dict[str, Any]: dictionary with model data ready for API submission.
        """
        exclude = set() if include_read_only else set(self._meta.read_only_fields)

        return self.model_dump(
            exclude=exclude,
            exclude_none=exclude_none,
            exclude_unset=exclude_unset,
        )

    @classmethod
    def create(cls, **kwargs: Any) -> Self:
        """
        Factory method to create a new model instance.

        Args:
            **kwargs: Field values to set.

        Returns:
            A new model instance.
        """
        # TODO save
        return cls(**kwargs)

    def update(self, **kwargs: Any) -> Self:
        """
        Update this model with new values.

        Args:
            **kwargs: New field values.

        Returns:
            Self with updated values.
        """
        # TODO save
        return self.model_copy(update=kwargs)

    def is_new(self) -> bool:
        """
        Check if this model represents a new (unsaved) object.

        Returns:
            True if the model is new, False otherwise.
        """
        return self.id == 0

    def __str__(self) -> str:
        """
        Human-readable string representation.

        Returns:
            A string representation of the model.
        """
        return f"{self._meta.name.capitalize()} #{self.id}"
