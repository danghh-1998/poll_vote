class BaseError(Exception):
    err_detail = 'An error occurred'
    err_code = None

    def __init__(self, custom_msg=None):
        self.err_detail = custom_msg or self.err_detail


class NotFoundError(BaseError):
    err_detail = 'Not found'
    err_code = 600


class ViolationWordError(BaseError):
    err_detail = 'Title contains violation words'
    err_code = 601


class VoteLimitationError(BaseError):
    err_detail = 'Poll must be 2-10 votes'
    err_code = 602


class PollConfigError(BaseError):
    err_detail = 'Poll not allowed to add vote'
    err_code = 603


class EditTitleError(BaseError):
    err_detail = 'The title can\'t be edited once people start voting'
    err_code = 604


class VotedError(BaseError):
    err_detail = 'You already voted'
    err_code = 605


class NotVotedError(BaseError):
    err_detail = 'You haven\'t voted yet'
    err_code = 606
