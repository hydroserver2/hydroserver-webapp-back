from ninja import Router, Query
from ninja.security import django_auth
from django.http import HttpResponse
from sensorthings.api.core.schemas import Filters
from sensorthings.api.core.main import SensorThingsRequest
from .schemas import FeatureOfInterestPostBody, FeatureOfInterestPatchBody, FeatureOfInterestListResponse, \
    FeatureOfInterestGetResponse


router = Router(tags=['Features Of Interest'])


@router.get(
    '/FeaturesOfInterest',
    # auth=django_auth,
    # response={200, FeatureOfInterestListResponse},
    url_name='list_feature_of_interest'
)
def get_features_of_interest(request: SensorThingsRequest, filters: Filters = Query(...)):
    """"""

    return {}


@router.get(
    '/FeaturesOfInterest({feature_of_interest_id})',
    # auth=django_auth,
    # response={200, ThingGetResponse},
    by_alias=True
)
def get_feature_of_interest(request, feature_of_interest_id: str):
    """"""

    return {}


@router.post(
    '/FeaturesOfInterest',
    # auth=django_auth,
    response={201: None}
)
def create_feature_of_interest(
        request: SensorThingsRequest,
        response: HttpResponse,
        feature_of_interest: FeatureOfInterestPostBody
):
    """
    Create a new Feature of Interest entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    feature_of_interest_id = request.engine.create(
        entity_body=feature_of_interest
    )

    response['location'] = request.engine.get_ref(
        entity_id=feature_of_interest_id
    )

    return 201, None


@router.patch(
    '/FeaturesOfInterest({feature_of_interest_id})',
    # auth=django_auth,
    response={204: None}
)
def update_feature_of_interest(
        request: SensorThingsRequest,
        feature_of_interest_id: str,
        feature_of_interest: FeatureOfInterestPatchBody
):
    """
    Update an existing Feature of Interest entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/properties" target="_blank">\
      Feature of Interest Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/feature-of-interest/relations" target="_blank">\
      Feature of Interest Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update(
        entity_id=feature_of_interest_id,
        entity_body=feature_of_interest
    )

    return 204, None


@router.delete(
    '/FeaturesOfInterest({feature_of_interest_id})',
    # auth=django_auth,
    response={204: None}
)
def delete_feature_of_interest(request: SensorThingsRequest, feature_of_interest_id: str):
    """
    Delete a Feature of Interest entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=feature_of_interest_id
    )

    return 204, None