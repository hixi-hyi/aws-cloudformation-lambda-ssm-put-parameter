# cfn-lambda-ssm-put-parameter
## Description
The `cfn-lambda-ssm-put-parameter` function is `SSM::Parameter` that support `SecureString` and `Region`

## When do you use it
* Put on secret infomation like `!GetAtt AWS::IAM::AccessKey.SecretAccessKey` into SSM::Parameter as SecureString.
* Put on `Arn` that can only be created in a specific region such as ACM into other region.

## Caution
The function can write a parameter to another region. so, it is different from cloudformation's usual usage.
If you want to use `cfn-lambda-ssm-put-paramter` function, first condider `cfn-lambda-ssm-get-parameter`.
Generally `get` operation is safer than `put` operation.


## Deploy
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#deploy)

## Usage
```
AccessKeySecret:
  Type: Custom::SsmParameter
  Properties:
    ServiceToken: !ImportValue cfn-lambda-ssm-put-parameter:LambdaArn
    Name: /user/hixi/access-key-secret
    Type: SecureString
    Value: !GetAtt HixiAccessKey.SecretAccessKey
    Region: !Ref AWS::Region
    Policies:
        Deletion:
            - Delete
```
## Parameters

### Name
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-name)
- ***Required:*** Yes
- ***Update requires:*** Replacement

### Type
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-type)
- The `SecureString` parameter type is supported.
- ***Required:*** Yes
- ***Update requires:*** Replacement


### Value (required) [No interruption]
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-value)
- ***Required:*** Yes
- ***Update requires:*** No interruption

### Region (optional) [Replacement]
- [Docs](https://docs.aws.amazon.com/general/latest/gr/rande.html)
- The region outside the default are also supported.
- Default parameter is `AWS::Region`.
- ***Required:*** No
- ***Update requires:*** Replacement

### Policies.Deletion (optional)
- Support values are `IgnoreError` and `Retain`.
  - `IgnoreError`
    - If you want to ignore some error.
  - `Retain`
    - If you want to retain the value in the SSM::Parameter.
- ***Required:*** No
- ***Update requires:*** No interruption


## ToDO
- Supports the kms
- Supports the `RoleArn` property on resource definition. The current role which defined by function may have strong permissions.

## Contributing
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#contributing)
