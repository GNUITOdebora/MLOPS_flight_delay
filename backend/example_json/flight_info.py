from pydantic import BaseModel, Field
from datetime import datetime

class FlightDataModel(BaseModel):
    MONTH: int = Field(..., example=1)
    ORIGIN_AIRPORT: str = Field(..., example="JFK")
    DESTINATION_AIRPORT: str = Field(..., example="LAX")
    DEPARTURE_DELAY: float = Field(..., example=15.2)
    SCHEDULED_TIME: float = Field(..., example=120.5)
    AIR_SYSTEM_DELAY: float = Field(..., example=5.0)
    SECURITY_DELAY: float = Field(..., example=2.0)
    AIRLINE_DELAY: float = Field(..., example=10.0)
    LATE_AIRCRAFT_DELAY: float = Field(..., example=8.0)
    WEATHER_DELAY: float = Field(..., example=0.5)
    DEPARTURE_TIME: datetime = Field(..., example="2024-05-14T08:30:00")
    SCHEDULED_ARRIVAL: datetime = Field(..., example="2024-05-14T10:30:00")
    AIRLINE: str = Field(..., example="AA")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "MONTH": 11,
                "ORIGIN_AIRPORT": "JFK",
                "DESTINATION_AIRPORT": "LAX",
                "DEPARTURE_DELAY": 15.2,
                "SCHEDULED_TIME": 120.5,
                "AIR_SYSTEM_DELAY": 5.0,
                "SECURITY_DELAY": 2.0,
                "AIRLINE_DELAY": 10.0,
                "LATE_AIRCRAFT_DELAY": 8.0,
                "WEATHER_DELAY": 0.5,
                "DEPARTURE_TIME": "2024-05-14T08:30:00",
                "SCHEDULED_ARRIVAL": "2024-05-14T10:30:00",
                "AIRLINE": "AA"
            }
        }
