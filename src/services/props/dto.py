from typing import Optional

from pydantic import BaseModel


class ClientServiceInput(BaseModel):
    requisite: str
    type: Optional[str] = None
