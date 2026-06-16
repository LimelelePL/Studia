from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Stop(Base):
    __tablename__ = "stops"

    stop_id: Mapped[int] = mapped_column(primary_key=True)
    stop_code: Mapped[str | None]
    stop_name: Mapped[str] = mapped_column(nullable=False)
    stop_lat: Mapped[float] = mapped_column(nullable=False)
    stop_lon: Mapped[float] = mapped_column(nullable=False)

    stop_times: Mapped[list[StopTime]] = relationship(back_populates="stop")


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[str] = mapped_column(primary_key=True)
    agency_id: Mapped[int | None]
    route_short_name: Mapped[str] = mapped_column(nullable=False)
    route_long_name: Mapped[str | None]
    route_desc: Mapped[str | None]
    route_type: Mapped[int | None]
    route_type2_id: Mapped[int | None]
    valid_from: Mapped[str | None]
    valid_until: Mapped[str | None]

    trips: Mapped[list[Trip]] = relationship(back_populates="route")


class Calendar(Base):
    __tablename__ = "calendar"
    __table_args__ = (
        CheckConstraint("monday IN (0, 1)", name="check_calendar_monday"),
        CheckConstraint("tuesday IN (0, 1)", name="check_calendar_tuesday"),
        CheckConstraint("wednesday IN (0, 1)", name="check_calendar_wednesday"),
        CheckConstraint("thursday IN (0, 1)", name="check_calendar_thursday"),
        CheckConstraint("friday IN (0, 1)", name="check_calendar_friday"),
        CheckConstraint("saturday IN (0, 1)", name="check_calendar_saturday"),
        CheckConstraint("sunday IN (0, 1)", name="check_calendar_sunday"),
    )

    service_id: Mapped[int] = mapped_column(primary_key=True)
    monday: Mapped[int] = mapped_column(nullable=False)
    tuesday: Mapped[int] = mapped_column(nullable=False)
    wednesday: Mapped[int] = mapped_column(nullable=False)
    thursday: Mapped[int] = mapped_column(nullable=False)
    friday: Mapped[int] = mapped_column(nullable=False)
    saturday: Mapped[int] = mapped_column(nullable=False)
    sunday: Mapped[int] = mapped_column(nullable=False)
    start_date: Mapped[str] = mapped_column(nullable=False)
    end_date: Mapped[str] = mapped_column(nullable=False)

    trips: Mapped[list[Trip]] = relationship(back_populates="calendar")


class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = (
        Index("idx_trips_route_id", "route_id"),
        Index("idx_trips_service_id", "service_id"),
    )

    trip_id: Mapped[str] = mapped_column(primary_key=True)
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.route_id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("calendar.service_id"), nullable=False)
    trip_headsign: Mapped[str | None]
    direction_id: Mapped[int | None]
    shape_id: Mapped[str | None]
    brigade_id: Mapped[str | None]
    vehicle_id: Mapped[str | None]
    variant_id: Mapped[str | None]

    route: Mapped[Route] = relationship(back_populates="trips")
    calendar: Mapped[Calendar] = relationship(back_populates="trips")
    stop_times: Mapped[list[StopTime]] = relationship(back_populates="trip")


class StopTime(Base):
    __tablename__ = "stop_times"
    __table_args__ = (
        PrimaryKeyConstraint("trip_id", "stop_sequence"),
        Index("idx_stop_times_stop_id", "stop_id"),
        Index("idx_stop_times_trip_id", "trip_id"),
    )

    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.trip_id"), nullable=False)
    arrival_time: Mapped[str] = mapped_column(nullable=False)
    departure_time: Mapped[str] = mapped_column(nullable=False)
    stop_id: Mapped[int] = mapped_column(ForeignKey("stops.stop_id"), nullable=False)
    stop_sequence: Mapped[int] = mapped_column(nullable=False)
    pickup_type: Mapped[int | None]
    drop_off_type: Mapped[int | None]

    trip: Mapped[Trip] = relationship(back_populates="stop_times")
    stop: Mapped[Stop] = relationship(back_populates="stop_times")
