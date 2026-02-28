from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):

    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):

    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field()
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):

    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(default_factory=datetime.now)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        senior_ranks = {Rank.commander, Rank.captain}
        has_senior = any(m.rank in senior_ranks for m in self.crew)
        if not has_senior:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = len([m for m in self.crew if m.years_experience > 4])
            if experienced / len(self.crew) < 0.5:
                raise ValueError(
                    "For long missions (> 365 days) need 50% experienced crew"
                    " (5+ years)"
                )

        inactive = [m.name for m in self.crew if not m.is_active]
        if inactive:
            raise ValueError(
                "All crew members must be active. "
                f"Inactive members: {inactive}"
            )

        return self


def display_mission(mission: SpaceMission) -> None:

    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) "
            f"- {member.specialization}"
        )


def main() -> None:

    print("Space Mission Crew Validation")
    print('=' * 40)

    try:
        crew1 = [
            CrewMember(
                member_id="C001",
                name="Sarah Connor",
                rank=Rank.commander,
                age=40,
                specialization="Mission Command",
                years_experience=15
            ),
            CrewMember(
                member_id="C002",
                name="John Smith",
                rank=Rank.lieutenant,
                age=32,
                specialization="Navigation",
                years_experience=8
            ),
            CrewMember(
                member_id="C003",
                name="Alice Johnson",
                rank=Rank.officer,
                age=28,
                specialization="Engineering",
                years_experience=5
            )
        ]
        mission1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now,
            duration_days=900,
            crew=crew1,
            budget_millions=2500.0
        )
        display_mission(mission1)
    except ValidationError as e:
        print("Expected validation error:")
        print(*[error['msg'] for error in e.errors()], sep='\n')
    except ValueError as e:
        print(f"Expected validation error:\n{e}")

    print(f"\n{'=' * 40}\n")

    try:
        crew2 = [
            CrewMember(
                member_id="C004",
                name="Bob",
                rank=Rank.cadet,
                age=22,
                specialization="Cleaning",
                years_experience=1
            )
        ]
        mission2 = SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Moon Base",
            destination="Moon",
            launch_date=datetime.now,
            duration_days=30,
            crew=crew2,
            budget_millions=500.0
        )
        display_mission(mission2)
    except ValidationError as e:
        print("Expected validation error:")
        print(*[error['msg'] for error in e.errors()], sep='\n')
    except ValueError as e:
        print(f"Expected validation error:\n{e}")


if __name__ == "__main__":
    main()
