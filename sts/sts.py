import os
import boto.sts


class STSHelper(object):
    def __init__(self, region, role_arn,
                 role_session_name, duration_seconds=3600):
        self.region = region
        self.role_arn = role_arn
        self.role_session_name = role_session_name
        self.duration_seconds = duration_seconds
        self.token = None

    def assume_role_env(self):
        credentials = self.assume_role_creds()
        if credentials:
            os.environ['AWS_ACCESS_KEY_ID'] = credentials.access_key
            os.environ['AWS_SECRET_ACCESS_KEY'] = credentials.secret_key
            os.environ['AWS_SECURITY_TOKEN'] = credentials.session_token

    def assume_role_creds(self):
        STSHelper.drop_role_env()
        conn = boto.sts.connect_to_region(self.region)
	try:
            self.token = conn.assume_role(self.role_arn,
                                          self.role_session_name)
            print('Got STS credentials for {}'.format(self.role_arn))
            return self.token.credentials
        except boto.exception.BotoServerError:
            print('Failed to get STS credentials for {}'.format(self.role_arn))
            return None

    @staticmethod
    def drop_role_env():
        env_vars = ['AWS_ACCESS_KEY_ID',
                    'AWS_SECRET_ACCESS_KEY',
                    'AWS_SECURITY_TOKEN']
        for var in env_vars:
            if os.environ.get(var):
                del os.environ[var]
