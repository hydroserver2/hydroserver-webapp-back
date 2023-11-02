from ninja import Path
from uuid import UUID
from typing import Optional
from datetime import datetime
from django.db import transaction, IntegrityError
from django.http import StreamingHttpResponse
from accounts.auth.jwt import JWTAuth
from accounts.auth.basic import BasicAuth
from accounts.auth.anonymous import anonymous_auth
from core.router import DataManagementRouter
from core.models import Datastream
from core.endpoints.unit.utils import query_units, build_unit_response
from core.endpoints.sensor.utils import query_sensors, build_sensor_response
from core.endpoints.observedproperty.utils import query_observed_properties, build_observed_property_response
from core.endpoints.processinglevel.utils import query_processing_levels, build_processing_level_response
from .schemas import DatastreamFields, DatastreamGetResponse, DatastreamPostBody, DatastreamPatchBody, \
     DatastreamMetadataGetResponse
from .utils import query_datastreams, get_datastream_by_id, build_datastream_response, check_related_fields, \
     generate_csv


router = DataManagementRouter(tags=['Datastreams'])


@router.dm_list('', response=DatastreamGetResponse)
def get_datastreams(request, modified_since: Optional[datetime] = None):
    """
    Get a list of Datastreams

    This endpoint returns a list of public Datastreams and Datastreams owned by the authenticated user if there is one.
    """

    datastream_query, _ = query_datastreams(user=request.authenticated_user, modified_since=modified_since)

    return [
        build_datastream_response(datastream) for datastream in datastream_query.all()
    ]


@router.dm_get('{datastream_id}', response=DatastreamGetResponse)
def get_datastream(request, datastream_id: UUID = Path(...)):
    """
    Get details for a Datastream

    This endpoint returns details for a Datastream given a Datastream ID.
    """

    datastream = get_datastream_by_id(
        user=request.authenticated_user,
        datastream_id=datastream_id,
        raise_http_errors=True
    )

    return 200, build_datastream_response(datastream)


@router.dm_post('', response=DatastreamGetResponse)
@transaction.atomic
def create_datastream(request, data: DatastreamPostBody):
    """
    Create a Datastream

    This endpoint will create a new Datastream.
    """

    check_related_fields(request.authenticated_user, data)

    datastream = Datastream.objects.create(
        **data.dict(include=set(DatastreamFields.__fields__.keys()))
    )

    datastream = get_datastream_by_id(
        user=request.authenticated_user,
        datastream_id=datastream.id,
    )

    return 201, build_datastream_response(datastream)


@router.dm_patch('{datastream_id}', response=DatastreamGetResponse)
@transaction.atomic
def update_datastream(request, data: DatastreamPatchBody, datastream_id: UUID = Path(...)):
    """
    Update a Datastream

    This endpoint will update an existing Datastream owned by the authenticated user and return the updated Datastream.
    """

    check_related_fields(request.authenticated_user, data)

    datastream = get_datastream_by_id(
        user=request.authenticated_user,
        datastream_id=datastream_id,
        require_ownership=True,
        raise_http_errors=True
    )

    datastream_data = data.dict(include=set(DatastreamFields.__fields__.keys()), exclude_unset=True)

    for field, value in datastream_data.items():
        setattr(datastream, field, value)

    datastream.save()

    datastream = get_datastream_by_id(user=request.authenticated_user, datastream_id=datastream.id)

    return 203, build_datastream_response(datastream)


@router.dm_delete('{datastream_id}')
def delete_datastream(request, datastream_id: UUID = Path(...)):
    """
    Delete a Datastream

    This endpoint will delete an existing Datastream if the authenticated user is the primary owner of the Datastream.
    """

    datastream = get_datastream_by_id(
        user=request.authenticated_user,
        datastream_id=datastream_id,
        require_primary_ownership=True,
        raise_http_errors=True
    )

    try:
        datastream.delete()
    except IntegrityError as e:
        return 409, str(e)

    return 204, None


@router.get(
    '{datastream_id}/csv',
    auth=[JWTAuth(), BasicAuth(), anonymous_auth],
    response={
        200: None,
        403: str,
        404: str
    }
)
def get_datastream_csv(request, datastream_id: UUID = Path(...)):

    datastream = get_datastream_by_id(
        user=request.authenticated_user,
        datastream_id=datastream_id,
        raise_http_errors=True
    )

    response = StreamingHttpResponse(generate_csv(datastream), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="hello_world.csv"'

    return response


@router.get(
    '{datastream_id}/metadata',
    auth=[JWTAuth(), BasicAuth(), anonymous_auth],
    response={
        200: DatastreamMetadataGetResponse,
        403: str,
        404: str
    },
    by_alias=True
)
def get_datastream_metadata(request, datastream_id: UUID = Path(...), include_assignable_metadata: bool = False):

    datastream = get_datastream_by_id(
        user=request.authenticated_user,
        datastream_id=datastream_id,
        raise_http_errors=True
    )

    primary_owner = next(iter([
        associate.person for associate in datastream.thing.associates.all()
        if associate.is_primary_owner is True
    ]), None)

    metadata_query_args = {
        'user': primary_owner,
        'require_ownership': True
    }

    if include_assignable_metadata is False:
        metadata_query_args['datastream_ids'] = [datastream_id]

    units, _ = query_units(**metadata_query_args)
    sensors, _ = query_sensors(**metadata_query_args)
    processing_levels, _ = query_processing_levels(**metadata_query_args)
    observed_properties, _ = query_observed_properties(**metadata_query_args)

    unit_data = [build_unit_response(unit) for unit in units.all()]
    sensor_data = [build_sensor_response(sensor) for sensor in sensors.all()]
    processing_level_data = [build_processing_level_response(pl) for pl in processing_levels.all()]
    observed_property_data = [build_observed_property_response(op) for op in observed_properties.all()]

    return 200, {
        'units': unit_data,
        'sensors': sensor_data,
        'processing_levels': processing_level_data,
        'observed_properties': observed_property_data
    }
