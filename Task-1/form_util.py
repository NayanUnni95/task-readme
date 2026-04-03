from enum import Enum


class QuestionKey(Enum):
    FIELD_ID = 'id'
    FIELD_TYPE = 'type'
    FIELD_TITLE = "title"
    HIDDEN = 'hidden'
    FIELD_UNIQUE = 'unique'
    TEAM_FIELD = 'team_field'
    PLACEHOLDER = 'placeholder'
    FIELD_REQUIRED = 'required'
    ADMIN_FIELD = 'admin_field'
    FIELD_KEY = 'field_key'
    DESCRIPTION = "description"
    PAGE_NUMBER = 'page_num'
    FIELD_OPTIONS = 'options'
    VALIDATE = 'validate'
    PROPERTY = "property"
    CONDITIONS = "conditions"

    @staticmethod
    def get_all_question_keys():
        return [question_key.value for question_key in QuestionKey]


class QuestionPropertyKey(Enum):
    FILE_SIZE = 'file_size'
    EXTENSION_TYPES = 'extension_types'
    MAX_NO_OF_FILES = 'max_no_of_files'
    TEXT_MAX_LENGTH = 'max_length'
    TEXT_MIN_LENGTH = 'min_length'


class QuestionTypes(Enum):
    SINGLE_SELECT = "singleselect"
    MULTI_SELECT = "multiselect"
    RADIO_BUTTON = "radio"
    CHECKBOX = "checkbox"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    TEXT_AREA = "textarea"
    TEXT = "text"
    NUMBER = "number"
    PHONE_NUMBER = "phone"
    EMAIL = "email"
    FILE = "file"
    RATING = "rating"
    URL = "url"

    @staticmethod
    def get_all_form_types():
        return [form_type.value for form_type in QuestionTypes]


class DefaultFormFieldsKeys(Enum):
    NAME = "name"
    EMAIL = "email"
    PHONE_NUMBER = "phone"
    CATEGORY = "category"
    ORGANIZATION = "organization"


class ConditionalQuestionFields(Enum):
    FIELD = "field"
    VALUE = "value"
    OPERATOR = "operator"
    ACTION = "action"

    @staticmethod
    def get_all_conditional_question_fields():
        return [c.value for c in ConditionalQuestionFields]


class ConditionalQuestionOperator(Enum):
    EQUAL = "="
    NOT_EQUAL = "!="
    IN = "in"
    NOT_IN = "not in"
    EMPTY = "empty"
    NOT_EMPTY = "not empty"
    CONTAINS = "contains"
    NOT_CONTAINS = "not contains"
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    @staticmethod
    def get_all_operators():
        return [operator.value for operator in ConditionalQuestionOperator]