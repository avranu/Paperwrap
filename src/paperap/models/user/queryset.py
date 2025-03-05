"""




----------------------------------------------------------------------------

   METADATA:

       File:    queryset.py
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

from typing import Any, TYPE_CHECKING
import logging
from paperap.models.abstract.queryset import QuerySet

if TYPE_CHECKING:
    from paperap.models.user.model import User, Group

logger = logging.getLogger(__name__)


class UserQuerySet(QuerySet["User"]):
    """
    A lazy-loaded, chainable query interface for Paperless NGX resources.

    QuerySet provides pagination, filtering, and caching functionality similar to Django's QuerySet.
    It's designed to be lazy - only fetching data when it's actually needed.
    """


class GroupQuerySet(QuerySet["Group"]):
    """
    A lazy-loaded, chainable query interface for Paperless NGX resources.

    QuerySet provides pagination, filtering, and caching functionality similar to Django's QuerySet.
    It's designed to be lazy - only fetching data when it's actually needed.
    """
