from qiniu import Auth

from settings import ENV_QINIU_AK
from settings import ENV_QINIU_DEFAULT_BUCKET
from settings import ENV_QINIU_SK
from settings import QINIU_BUCKET_URL_MAP

q = Auth(ENV_QINIU_AK, ENV_QINIU_SK)


# q = Auth('pNm_9YXxDdSL8sx51Oy0BQ32j76yrEfPPFeVo6A5', 'xaYOcSzlrPp6IC3U1x3VV3amWZ9CqWV0Y7yXXg-2')


def get_qiniu_token(prefix: str = '',
                    bucket_name: str = ENV_QINIU_DEFAULT_BUCKET):
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
    base_url = QINIU_BUCKET_URL_MAP.get(bucket_name, '')

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
