# STS

### Summary

STS is used to provide an application with temporary security credentials.
Use of STS avoids the need to distribute hardcoded AWS security credentials
with your application and the associated key management nightmare.
STS credentials are short lived so there is no need to manually rotate them.

### Uses

One use case for STS is providing cross account access.

For example, if Jenkins is running in your infrastructure account, but needs
to launch an instance in your development account, you can provide cross account
access using STS. By setting up the proper IAM roles in both accounts and
using STS, Jenkins can perform specified actions in the devlopment account.

### Sample Application

The sample application is running on an instance with the following IAM role
(arn:aws:iam::\<account-id\>:role/assumerole):
```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["sts:AssumeRole"],
    "Resource": [
      "arn:aws:iam::<account-id>:role/read-only"
    ]
  }]
}
```

The application attempts to describe-instances, but this will fail.
The application then acquires STS credentials for the read only IAM role
(arn:aws:iam::<account-id>:role/read-only)
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:Describe*",
      "Resource": "*"
    }
  ]
}
```

The read only IAM role has the following trust policy:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com",
        "AWS": "arn:aws:iam::<account-id>:role/assumerole"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

The application again attempts to describe-instances and succeeds.


### Cross Account Access

For cross account use, the IAM policy in the granting account must specify
trusted entities that are allowed to assume the role.
In the AWS IAM Role console for the role that will be assumed, Edit Trust
Relationship. This allows you to specify the IAM role(s) that may assume
the role you are editing.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com",
        "AWS": "arn:aws:iam::<other-account-id>:role/<role-in-other-account>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
