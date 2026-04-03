import uuid
from enum import Enum


class SubmissionStatus(Enum):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    IN_REVIEW = 'In Review'
    WITHDRAWN = 'Withdrawn'
    BLOCKED = 'Blocked'

    @staticmethod
    def get_all_status_types():
        return [roles.value for roles in SubmissionStatus]

    @staticmethod
    def get_send_mail_status_types():
        return [
            SubmissionStatus.ACCEPTED.value,
            SubmissionStatus.REJECTED.value,
        ]


class EventStatus(Enum):
    DRAFT = 'Draft'
    PUBLISHED = 'Published'
    COMPLETED = 'Completed'
    PARTICIPATING = 'Participating'

    @staticmethod
    def get_all_status_types():
        return [status.value for status in EventStatus]


class DefaultForms(Enum):
    PRIMARY_FORM_TITLE = "Primary Speaker Submission Form"

    @staticmethod
    def generate_default_form():
        return [
            {
                "id": str(uuid.uuid4()),
                "type": "text",
                "title": "Name",
                "hidden": False,
                "unique": False,
                "options": [],
                "page_num": 1,
                "property": {},
                "required": True,
                "field_key": "name",
                "conditions": {},
                "team_field": False,
                "description": None,
                "placeholder": ""
            },
            {
                "id": str(uuid.uuid4()),
                "type": "phone",
                "title": "Phone Number",
                "hidden": False,
                "unique": False,
                "options": [],
                "page_num": 1,
                "property": {},
                "required": True,
                "field_key": "phone",
                "conditions": {},
                "team_field": False,
                "description": None,
                "placeholder": ""
            },
            {
                "id": str(uuid.uuid4()),
                "type": "email",
                "title": "Email",
                "hidden": False,
                "unique": False,
                "options": [],
                "page_num": 1,
                "property": {},
                "required": True,
                "field_key": "email",
                "conditions": {},
                "team_field": False,
                "description": None,
                "placeholder": ""
            }
        ]

    @staticmethod
    def generate_secondary_form():
        return [
            {
                "id": str(uuid.uuid4()),
                "type": "text",
                "title": "text",
                "hidden": False,
                "unique": False,
                "options": [],
                "page_num": 1,
                "property": {},
                "required": True,
                "field_key": "text",
                "conditions": {},
                "team_field": False,
                "description": None,
                "placeholder": ""
            }
        ]


class ScheduleStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'

    @staticmethod
    def get_all_status_types():
        return [status.value for status in ScheduleStatus]


class StaticPlaceHolders(Enum):
    NAME = 'name'
    TITLE = 'title'
    REJECTION_REASON = 'rejection_reason'
    SECONDARY_FORM_URL = 'secondary_form_url'


class FormType(Enum):
    COMMON = 'Common'