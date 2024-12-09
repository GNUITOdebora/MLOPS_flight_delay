from pydantic import BaseModel, Field
from typing import Dict, Optional

class FlightDataModel(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Month of the flight (1-12)")
    origin_airport: int = Field(..., description="Encoded origin airport")
    destination_airport: int = Field(..., description="Encoded destination airport")
    departure_delay: float = Field(..., description="Delay in departure time (minutes)")
    scheduled_time: Dict[str, int] = Field(
        ..., description="Scheduled departure time in hours and minutes"
    )
    scheduled_arrival: Dict[str, int] = Field(
        ..., description="Scheduled arrival time in hours and minutes"
    )
    air_system_delay: float = Field(..., description="Air system delay (minutes)")
    security_delay: float = Field(..., description="Security delay (minutes)")
    airline_delay: float = Field(..., description="Airline delay (minutes)")
    late_aircraft_delay: float = Field(..., description="Delay caused by late aircraft (minutes)")
    airlines: Dict[str, float] = Field(
        ..., description="Dictionary containing airline-specific encoded values"
    )

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "MONTH": 11,
                "ORIGIN_AIRPORT": 496,
                "DESTINATION_AIRPORT": 450,
                "DEPARTURE_DELAY": -6.0,
                "SCHEDULED_TIME": 68 ,
                "SCHEDULED_ARRIVAL":2140,
                "AIR_SYSTEM_DELAY": 0.0,
                "SECURITY_DELAY": 0.0,
                "AIRLINE_DELAY": 1.0,
                "LATE_AIRCRAFT_DELAY": 0.0,
                "WEATHER_DELAY": 0.0,
                "DEPARTURE_TIME": {"HOURS": 1, "MINUTES": 20},
                "AIRLINE": "WN"
            }
        }
