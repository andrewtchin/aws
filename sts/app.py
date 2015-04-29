import argparse

import boto.ec2

import sts


def describe_instances(region):
    ec2_conn = boto.ec2.connect_to_region(region)
    try:
        reservations = ec2_conn.get_all_reservations()
        for reservation in reservations:
            print('Instance: {}'.format(reservation.instances))
    except:
        print('Failed to get reservations.')


def parse_args():
    parser = argparse.ArgumentParser(description='Demonstrate STS.')
    parser.add_argument('--region',
                        help='AWS region to connect to.')
    parser.add_argument('--assumerole',
                        help='ARN of the IAM role to assume.')
    return parser.parse_args()


def main():
    args = parse_args()
    region = args.region
    role_arn = args.assumerole

    print('Attempt to get reservations.')
    describe_instances(region)

    print('Assume role: {}'.format(role_arn))
    creds = sts.STSHelper(region, role_arn, 'test_session')
    creds.assume_role_env()

    print('Attempt to get reservations.')
    describe_instances(region)


if __name__ == '__main__':
    main()
