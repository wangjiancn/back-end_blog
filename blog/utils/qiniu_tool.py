from django.conf import settings
from qiniu import Auth

q = Auth(settings.ENV_QINIU_AK, settings.ENV_QINIU_SK)


def get_qiniu_token(prefix: str = '',
                    bucket_name: str = settings.ENV_QINIU_DEFAULT_BUCKET):
    """获取七牛TOKEN

    Doc:
        http://developer.qiniu.com/docs/v6/api/reference/security/put-policy.html

    :param prefix:
    :param bucket_name: 要上传的空间
    :return:
    """
    prefix = prefix.strip('/')
    if prefix:
        save_key = f"{prefix}/$(etag)$(ext)"
    else:
        save_key = '$(etag)$(ext)'
    base_url = settings.QINIU_BUCKET_URL_MAP.get(bucket_name, '')

    policy = {
        'saveKey': save_key,
        'returnBody': """{{
            "hash": $(hash),
            "key": $(key),
            "fsize": $(fsize),
            "exif": $(exif),
            "ext": $(ext),
            "msg":"OK",
            "code":0,
            "size": $(fsize),
            "name": $(fname),
            "url": "{}/$(key)"
        }}""".replace(' ', '').replace('\n', '').format(base_url)
    }
    token = q.upload_token(bucket_name, policy=policy)
    return token
