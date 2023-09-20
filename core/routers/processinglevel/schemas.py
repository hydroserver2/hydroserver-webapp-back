from ninja import Schema
from uuid import UUID
from sensorthings.validators import allow_partial


class ProcessingLevelID(Schema):
    id: UUID


class ProcessingLevelFields(Schema):
    code: str
    definition: str = None
    explanation: str = None


class ProcessingLevelGetResponse(ProcessingLevelFields, ProcessingLevelID):
    pass

    class Config:
        allow_population_by_field_name = True


class ProcessingLevelPostBody(ProcessingLevelFields):
    pass


@allow_partial
class ProcessingLevelPatchBody(ProcessingLevelFields):
    pass