from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):

    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(default_factory=datetime.now)
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(None, max_length=200)


def display_station(station: SpaceStation) -> None:

    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    status = 'Operational' if station.is_operational else 'Non-operational'
    print(f"Status: {status}")


def main() -> None:

    print("Space Station Data Validation")
    print('=' * 40)

    try:
        station1 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
        )
        display_station(station1)
    except ValidationError as e:
        print("Expected validation error:")
        print(*[error['msg'] for error in e.errors()], sep='\n')
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        print(f"\n{'=' * 40}")

    try:
        station2 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=155,
            power_level=85.5,
            oxygen_level=92.3,
        )
        display_station(station2)
    except ValidationError as e:
        print("Expected validation error:")
        print(*[error['msg'] for error in e.errors()], sep='\n')


if __name__ == "__main__":
    main()
