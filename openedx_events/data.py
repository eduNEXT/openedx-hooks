"""
Data attributes for events within the architecture subdomain `learning`.

These attributes follow the form of attr objects specified in OEP-49 data
pattern.
"""
import socket
from datetime import datetime, timezone
from uuid import UUID, uuid1

import attr
from django.conf import settings

import openedx_events


def _ensure_utc_time(_, attribute, value):
    """
    Ensure the value is a UTC datetime.

    Note: Meant to be used along-side an instance_of attr validator.
    """
    if value.tzinfo and value.tzinfo == timezone.utc:
        return
    raise ValueError(f"'{attribute.name}' must have timezone.utc")


@attr.s(frozen=True)
class EventsMetadata:
    """
    Attributes defined for Open edX Events metadata object.

    The attributes defined in this class are a subset of the
    OEP-41: Asynchronous Server Event Message Format.

    Arguments:
        id (UUID): event identifier.
        event_type (str): name of the event.
        minorversion (int): (optional) version of the event type. Defaults to 0.
        source (str): logical source of an event.
        sourcehost (str): physical source of the event.
        time (datetime): (optional) timestamp when the event was sent with
            UTC timezone. Defaults to current time in UTC. See OEP-41 for
            details.
        sourcelib (tuple of ints): Open edX Events library version. A tuple was
            selected so that version comparisons don't have to worry about
            lexical ordering of strings (e.g. '0.9.0' vs. '0.10.0').
    """

    id = attr.ib(type=UUID, init=False)
    event_type = attr.ib(type=str)
    minorversion = attr.ib(type=int, default=None, converter=attr.converters.default_if_none(0))
    source = attr.ib(type=str, init=False)
    sourcehost = attr.ib(type=str, init=False)
    current_utc_time = datetime.now(timezone.utc)
    time = attr.ib(
        type=datetime,
        default=None,
        converter=attr.converters.default_if_none(attr.Factory(lambda: datetime.now(timezone.utc))),
        validator=attr.validators.optional([attr.validators.instance_of(datetime), _ensure_utc_time]),
    )
    sourcelib = attr.ib(type=tuple, init=False)

    def __attrs_post_init__(self):
        """
        Post-init hook that generates metadata for the Open edX Event.
        """
        # Have to use this to get around the fact that the class is frozen
        # (which we almost always want, but not while we're initializing it).
        # Taken from edX Learning Sequences data file.
        object.__setattr__(self, "id", uuid1())
        object.__setattr__(
            self,
            "source",
            "openedx/{service}/web".format(
                service=getattr(settings, "SERVICE_VARIANT", "")
            ),
        )
        object.__setattr__(self, "sourcehost", socket.gethostname())
        object.__setattr__(
            self, "sourcelib", tuple(map(int, openedx_events.__version__.split(".")))
        )
