# AWS Boto3 Automation: EC2 Lifecycle Management

This repository contains Python Boto3 scripts deployed on AWS Lambda to automate the starting and stopping of EC2 instances based on resource tags.

## 📂 Repository Structure

*   **`assignment-1/`**: Lambda function to automatically stop/start EC2 instances based on tags.
*   **`assignment-2/`**: Lambda function for Assignment 2.
*   **`screenshots/`**: Visual verification of AWS environment setup and execution.

---

## 🛠️ Step 1: EC2 Instance Setup

To test this automation, two EC2 instances are configured in the AWS Management Console with specific resource tags:

1.  **Instance 1 (Auto-Stop Target)**
    *   **Name**: `Auto-Stop`
    *   **Instance type**: `t3.micro`
    *   **Tag**: Key = `Action`, Value = `Auto-Stop`
    *   **Initial State**: `Running`

2.  **Instance 2 (Auto-Start Target)**
    *   **Name**: `Auto-Start`
    *   **Instance type**: `t3.micro`
    *   **Tag**: Key = `Action`, Value = `Auto-Start`
    *   **Initial State**: `Stopped`

---

## 🔐 Step 2: Create IAM Role for Lambda

To allow the Lambda function to interact with your EC2 instances, an IAM Execution Role must be configured:

1.  **Trusted Entity**: AWS Service (`Lambda`)
2.  **Permissions Policy**: `AmazonEC2FullAccess`
3.  **Role Name**: `LambdaEC2ManagementRole`

---

## 🚀 Step 3: Create the AWS Lambda Function

A Lambda function is configured to execute the Python Boto3 automation script:

1.  **Function Name**: `EC2-Auto-Manager`
2.  **Runtime**: `Python 3.14`
3.  **Execution Role**: `LambdaEC2ManagementRole` (Selected via Custom execution role settings)

---

## 📸 Deployment Screenshots

### EC2 Dashboard Setup
Below is the verification screenshot showing both target EC2 instances in their correct initial states before running the automation script.

![EC2 Setup Verification](./screenshots/ec2_setup.png)

### IAM Role Verification
Below is the verification screenshot showing the `LambdaEC2ManagementRole` successfully created with the `AmazonEC2FullAccess` policy attached.

![IAM Role Setup Verification](./screenshots/iam_role_setup.png)

### Lambda Function Creation List
Below is the verification screenshot confirming the successful initialization of the `EC2-Auto-Manager` function within the AWS console environment.

![Lambda Function Configuration](./screenshots/lambda_setup.png)
---

## 💻 Step 4: Write the Boto3 Python Code

The Lambda function logic is implemented using Python and Boto3 inside `assignment-1/lambda_function.py`. The script uses target resource filters to inspect the cloud environment, identify instances based on their `Action` tags, and adjust their running state safely.
