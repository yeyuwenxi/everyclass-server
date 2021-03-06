from everyclass.server.utils import base_exceptions

"""Registration and Login"""


class UserNotExists(base_exceptions.InvalidRequestException):
    """密码验证时，用户不存在"""

    def __init__(self):
        super().__init__("用户未注册，请先注册", 4100)


class WrongPassword(base_exceptions.InvalidRequestException):
    """登录时密码错误"""

    def __init__(self):
        super().__init__("密码错误", 4101)


class AlreadyRegisteredError(base_exceptions.InvalidRequestException):
    """用户已存在，不允许再注册"""

    def __init__(self, ):
        super().__init__("用户已经注册了，请直接登录", 4102)


class InvalidTokenError(base_exceptions.InvalidRequestException):
    """邮件token无效"""

    def __init__(self):
        super().__init__("邮件token无效", 4103)


class IdentityVerifyRequestNotFoundError(base_exceptions.InvalidRequestException):
    """验证请求不存在"""

    def __init__(self):
        super().__init__("验证请求不存在", 4104)


class IdentityVerifyRequestStatusError(base_exceptions.InvalidRequestException):
    """当前VerificationRequest的状态并非STATUS_TKN_PASSED"""

    def __init__(self):
        super().__init__("状态异常", 4105)


class PasswordTooWeakError(base_exceptions.InvalidRequestException):
    """注册时密码太弱"""

    def __init__(self):
        super().__init__("密码过弱，请设置更强的密码", 4106)


"""visiting"""


class LoginRequired(base_exceptions.PermissionException):
    """需要登录才能访问"""

    def __init__(self):
        super().__init__("登录后即可访问此用户课表", 4107)


class PermissionAdjustRequired(base_exceptions.PermissionException):
    """仅自己可见的用户访问实名互访的用户，拒绝，要求调整自己的权限"""

    def __init__(self):
        super().__init__("请调整自己的课表权限为实名互访再访问此用户", 4108)


"""granting"""


class HasPendingRequest(base_exceptions.InvalidRequestException):
    """有处于pending状态的request，不允许新创建grant请求"""


class AlreadyGranted(base_exceptions.InvalidRequestException):
    """已经授权了，不能再创建授权请求"""


class RecordNotFound(base_exceptions.InvalidRequestException):
    """条目未找到，可能是请求错误"""


class NoPermissionToAccept(base_exceptions.PermissionException):
    """不是发向自己的请求，无权同意"""
