import elasticapm
from flask import Blueprint, current_app as app, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from everyclass.server import logger
from everyclass.server.db.dao import IdentityVerificationDAO, UserDAO
from everyclass.server.utils.rpc import HttpRpc

user_bp = Blueprint('user', __name__)


@user_bp.route('/login')
def login():
    """
    登录页

    判断学生是否未注册，若已经注册，渲染登陆页。否则跳转到注册页面。
    """
    if not request.args.get('sid'):
        return render_template('common/badRequest.html')

    # contact api-server to get original sid
    with elasticapm.capture_span('rpc_query_student'):
        rpc_result = HttpRpc.call_with_handle_flash('{}/v1/student/{}'.format(app.config['API_SERVER_BASE_URL'],
                                                                              request.args.get('sid')))
        if isinstance(rpc_result, Response):
            return rpc_result
        api_response = rpc_result

    # if not registered, redirect to register page
    if not UserDAO.exist(api_response['sid']):
        return redirect(url_for('user.register', sid=request.args.get('sid')))

    return render_template('user/login.html',
                           name=api_response['name'])


@user_bp.route('/register')
def register():
    """学生注册页面"""
    from flask import flash

    if not request.args.get('sid'):
        return render_template('common/badRequest.html')

    # if registered, redirect to login page
    if UserDAO.exist(request.args.get('sid')):
        flash('你已经注册了，请直接登录。')
        return redirect('user.login')

    return render_template('user/register.html', sid=request.args.get('sid'))  # todo register page


@user_bp.route('/register/byEmail', methods=['GET'])
def register_by_email():
    """学生注册-邮件"""
    if not request.args.get('sid'):
        return render_template('common/badRequest.html')
    # todo


@user_bp.route('/register/byPassword', methods=['GET'])
def register_by_email():
    """学生注册-密码"""
    pass
    # todo


@user_bp.route('/emailVerification')
def email_verification():
    """邮箱验证"""
    if not request.args.get("token"):
        logger.warn("Email verification with no token.")
        return redirect("main.main")

    rpc_result = HttpRpc.call_with_handle_flash('{}/verify_email_token'.format(app.config['AUTH_BASE_URL'],
                                                                               request.args.get('token')),
                                                data={"email_token": request.args.get("token")})
    if isinstance(rpc_result, Response):
        return rpc_result
    api_response = rpc_result

    if api_response['success']:
        # email verification passed
        IdentityVerificationDAO.email_token_mark_passed(api_response['request_id'])
        return render_template('user/emailVerificationProceed.html', request_id=api_response['request_id'])
    else:
        # token invalid
        # todo token invalid page
        return {'success': "false"}
