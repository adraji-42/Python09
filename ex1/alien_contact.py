from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):

    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime = Field(default_factory=datetime.now)
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType = Field()
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_contact(self) -> "AlienContact":

        if self.contact_id[:2] != "AC":
            raise ValueError("Contact ID must start with AC")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )

        return self


def display_contact(contact: AlienContact) -> None:

    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: {contact.message_received}")


def main() -> None:

    print("Alien Contact Log Validation")
    print('=' * 40)

    try:
        contact1 = AlienContact(
            contact_id="AC_2024_001",
            contact_type=ContactType.radio,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )
        display_contact(contact1)
    except ValidationError as e:
        print("Expected validation error:")
        print(*[error['msg'] for error in e.errors()], sep='\n')
    except ValueError as e:
        print(f"Expected validation error:\n{e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        print(f"\n{'=' * 40}")

    try:
        contact2 = AlienContact(
            contact_id="AC_2020_983",
            contact_type=ContactType.telepathic,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli"
        )
        display_contact(contact2)
    except ValidationError as e:
        print("Expected validation error:")
        print(*[error['msg'] for error in e.errors()], sep='\n')
    except ValueError as e:
        print(f"Expected validation error:\n{e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
