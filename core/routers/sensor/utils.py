from ninja.errors import HttpError
from typing import List, Optional
from uuid import UUID
from django.db.models import Q
from django.db.models.query import QuerySet
from core.models import Person, Sensor
from .schemas import SensorFields


def apply_sensor_auth_rules(
        user: Person,
        sensor_query: QuerySet,
        require_ownership: bool = False,
        check_result: bool = False
) -> (QuerySet, bool):

    result_exists = sensor_query.exists() if check_result is True else None

    if not user and require_ownership is True:
        raise HttpError(403, 'You are not authorized to access this Sensor.')

    if user and require_ownership is True:
        sensor_query = sensor_query.filter(Q(person=user))

    return sensor_query, result_exists


def query_sensors(
        user: Person,
        check_result_exists: bool = False,
        require_ownership: bool = False,
        sensor_ids: Optional[List[UUID]] = None,
        datastream_ids: Optional[List[UUID]] = None
):

    sensor_query = Sensor.objects

    if sensor_ids:
        sensor_query = sensor_query.filter(id__in=sensor_ids)

    if datastream_ids:
        sensor_query = sensor_query.filter(datastreams__id__in=datastream_ids)

    sensor_query, result_exists = apply_sensor_auth_rules(
        user=user,
        sensor_query=sensor_query,
        require_ownership=require_ownership,
        check_result=check_result_exists
    )

    return sensor_query, result_exists


def check_sensor_by_id(
        user: Person,
        sensor_id: UUID,
        require_ownership: bool = False,
        raise_http_errors: bool = False
):

    sensor_query, sensor_exists = query_sensors(
        user=user,
        sensor_ids=[sensor_id],
        require_ownership=require_ownership,
        check_result_exists=True
    )

    sensor = sensor_query.exists()

    if raise_http_errors and not sensor_exists:
        raise HttpError(404, 'Sensor not found.')
    if raise_http_errors and sensor_exists and not sensor:
        raise HttpError(403, 'You do not have permission to perform this action on this Sensor.')

    return sensor


def get_sensor_by_id(
        user: Person,
        sensor_id: UUID,
        require_ownership: bool = False,
        raise_http_errors: bool = False
):

    sensor_query, sensor_exists = query_sensors(
        user=user,
        sensor_ids=[sensor_id],
        require_ownership=require_ownership,
        check_result_exists=True
    )

    sensor = next(iter(sensor_query.all()), None)

    if raise_http_errors and not sensor_exists:
        raise HttpError(404, 'Sensor not found.')
    if raise_http_errors and sensor_exists and not sensor:
        raise HttpError(403, 'You do not have permission to perform this action on this Sensor.')

    return sensor


def build_sensor_response(sensor):
    return {
        'id': sensor.id,
        **{field: getattr(sensor, field) for field in SensorFields.__fields__.keys()},
    }