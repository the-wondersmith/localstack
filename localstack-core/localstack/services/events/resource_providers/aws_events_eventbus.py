# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class EventsEventBusProperties(TypedDict):
    Name: Optional[str]
    Arn: Optional[str]
    EventSourceName: Optional[str]
    Id: Optional[str]
    Policy: Optional[str]
    Tags: Optional[list[TagEntry]]


class TagEntry(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EventsEventBusProvider(ResourceProvider[EventsEventBusProperties]):
    TYPE = "AWS::Events::EventBus"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EventsEventBusProperties],
    ) -> ProgressEvent[EventsEventBusProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - Name

        Create-only properties:
          - /properties/Name
          - /properties/EventSourceName

        Read-only properties:
          - /properties/Id
          - /properties/Policy
          - /properties/Arn

        """
        model = request.desired_state
        events = request.aws_client_factory.events

        response = events.create_event_bus(Name=model["Name"])
        model["Arn"] = response["EventBusArn"]
        model["Id"] = model["Name"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EventsEventBusProperties],
    ) -> ProgressEvent[EventsEventBusProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EventsEventBusProperties],
    ) -> ProgressEvent[EventsEventBusProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        events = request.aws_client_factory.events

        events.delete_event_bus(Name=model["Name"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[EventsEventBusProperties],
    ) -> ProgressEvent[EventsEventBusProperties]:
        """
        Update a resource


        """
        raise NotImplementedError

    def list(
        self,
        request: ResourceRequest[EventsEventBusProperties],
    ) -> ProgressEvent[EventsEventBusProperties]:
        resources = request.aws_client_factory.events.list_event_buses()
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_models=[
                EventsEventBusProperties(Name=resource["Name"])
                for resource in resources["EventBuses"]
            ],
        )
