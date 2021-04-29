## 允许AWS主账号访问同一个Organization下的多个子账号资源

## 准备工作

* 允许AWS主账号访问同一个Organization下的多个子账号资源，需要在子账号一个角色，本项目中将使用CloudFormation模板部署这个角色，以Stackset的方式部署在AWS Organization中的所有子账号中。具体角色模板请参考template文件夹中的ReadOnlyAccessRole.yml文件，data文件夹中的ReadOnlyAccessRole.json文件为角色的CloudFormation模板所需要的参数，其中AdministratorAccountId为主账号ID，如果脚本在本地工作机运行则将CreateInstanceRole参数设置为No。 

* 步骤中脚本需要在主账号中以管理员身份执行。

## 步骤

### 1. 在所有需要访问的子账号中部署ReadOnlyAccessRole角色
```
python create_stackset_and_instances.py \
    --name ReadOnlyAccessRole \
    --template template/ReadOnlyAccessRole.yml \
    --parameters data/ReadOnlyAccessRole.json \
    --enabled_regions us-east-1 \
    --ou OU_ID

```
* 以上命令中--name参数指定的是CloudFormation模板名称，角色名称在ReadOnlyAccessRole.yml中定义
* 命令参数--enabled_regions指定启用角色的区域，由于AWS IAM为Global服务，只需指定us-east-1即可
* 命令参数--ou需要指定AWS Organization的ID，这个Organization中的全部子账号都会进行部署

### 2. 在主账号中创建一个新的角色，赋予如下policy，并attach给需要执行命令的EC2
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "*"
        }
    ]
}

```

### 3. 在主账号上需要执行命令的EC2上运行:
```
aws sts assume-role --role-arn "arn:aws:iam::[sub account id]:role/ReadOnlyAccessRole" --role-session-name "readonlyaccess"
```
* 请将[sub account id]替换为需要访问的子账号id

### 4. 利用上一步中得到的临时安全身份，访问子账号下资源
```
export AWS_ACCESS_KEY_ID=ASIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_SESSION_TOKEN=AQoDYXdzEJr...<remainder of security token>
aws ec2 describe-instances --region us-east-1
```
* 上述临时身份也可以使用其他方式使用，详见：https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html


