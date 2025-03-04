"""




----------------------------------------------------------------------------

   METADATA:

       File:    ui_settings.py
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

from typing import Any, Dict

from pydantic import BaseModel, Field

from paperap.models.base import PaperlessModel


class UISettings(PaperlessModel):
    """
    Represents UI settings in Paperless-NgX.
    """

    user: int
    settings: dict[str, Any]
