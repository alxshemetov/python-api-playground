from typing import Any

from pydantic import BaseModel, Field, RootModel, model_validator


# --- Request Body Models ---

class ArtistBase(BaseModel):
    first_name: str = Field(
        min_length=1,
        description="Artist's first name (must be non-empty)"
    )
    last_name: str = Field(
        min_length=1,
        description="Artist's last name (must be non-empty)"
    )
    birth_year: str = Field(
        min_length=1,
        description="Artist's birth year (must be a non-empty)"
    )


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(ArtistBase):
    user_id: str = Field(
        min_length=1,
        description="Artist's unique ID (must be non-empty)"
    )


# --- Response Models ---

class ArtistResponse(BaseModel):
    """Represents a single artist with named fields."""
    user_id: int
    first_name: str
    last_name: str
    birth_year: int

    @model_validator(mode='before')
    @classmethod
    def validate_from_list(cls, data: Any) -> Any:
        """
        Allows the model to be populated from a list.
        Converts [user_id, "first", "last", birth_year] into a dict.
        """
        if isinstance(data, list):
            try:
                # Convert the list to a dictionary for standard validation
                return {
                    'user_id': data[0],
                    'first_name': data[1],
                    'last_name': data[2],
                    'birth_year': data[3],
                }
            except (IndexError, TypeError):
                # Let the standard validator raise a clear error
                pass

                # Pass it on if it's already a dict or an invalid type
        return data


class ArtistCreateResponse(RootModel[int]):
    pass


class ArtistUpdateResponse(RootModel[bool]):
    pass


class ArtistDeleteResponse(RootModel[bool]):
    pass

# --- Error Response Models ---
