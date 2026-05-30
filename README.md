# AWS Boto3 Automation Portfolio

This repository contains Python Boto3 automation scripts designed to optimize cloud infrastructure, enforce security compliance, and handle automated backup lifecycles.

## 📂 Repository Structure

*   **`assignment-1/`**: Lambda function to automatically stop/start EC2 instances based on tags.
*   **`assignment-2/`**: Lambda function to automatically clean up old files in an S3 bucket based on retention rules.
*   **`assignment-3/`**: Lambda compliance worker to audit S3 bucket server-side encryption settings.
*   **`assignment-4/`**: Python script (`ebs_backup_manager.py`) for automated EBS snapshots and lifecycle maintenance.
*   **`screenshots/`**: Visual verification of AWS setups, console status changes, and script execution logs.

---

## 🛠️ Assignment 1: EC2 Lifecycle Management

Automates the starting and stopping of EC2 instances to reduce infrastructure operational costs based on specific runtime tags.

### Step 1: EC2 Instance Setup
Two target EC2 instances are configured in the AWS Management Console:
1.  **Instance 1 (Auto-Stop Target)**: Name = `Auto-Stop`, Type = `t3.micro`, Tag = `Action:Auto-Stop`, Initial State = `Running`.
2.  **Instance 2 (Auto-Start Target)**: Name = `Auto-Start`, Type = `t3.micro`, Tag = `Action:Auto-Start`, Initial State = `Stopped`.

### Step 2: Create IAM Role for Lambda
*   **Trusted Entity**: AWS Service (`Lambda`)
*   **Permissions Policy**: `AmazonEC2FullAccess`
*   **Role Name**: `LambdaEC2ManagementRole`

### Step 3: Create the AWS Lambda Function
*   **Function Name**: `EC2-Auto-Manager`
*   **Runtime**: `Python 3.14`
*   **Execution Role**: `LambdaEC2ManagementRole`

### Step 4: Write the Boto3 Python Code
The Lambda function logic is implemented inside `assignment-1/lambda_function.py`. The script targets resource filters to inspect the cloud environment, identify instances based on their `Action` tags, and adjust their running states safely.

### Step 5: Testing & Execution Results
The Lambda function was manually triggered using a default mock test event configuration. The runtime cleared out targets successfully.

#### 📸 Assignment 1 Screenshots
![EC2 Setup Verification](./screenshots/ec2_setup.png)
![IAM Role Setup Verification](./screenshots/iam_role_setup.png)
![Lambda Function Configuration](./screenshots/lambda_setup.png)
![Lambda Test Success](./screenshots/lambda_execution_success.png)
![EC2 Status Post Lambda](./screenshots/EC2_Status_Post_lambda_execution_success.png)

---

## 🪣 Assignment 2: Automated S3 Bucket Cleanup

Automated serverless script running on AWS Lambda using Boto3 to sweep an S3 bucket and permanently delete object files using a custom retention lifecycle policy.

### Step 1: S3 Bucket Setup
*   **Bucket Name**: `cleanup-test-bench-nagin`
*   **Object Seeding**: Uploaded multiple tracking testing files with visible timestamps.

### Step 2: Lambda IAM Role Configuration
*   **Trusted Entity**: AWS Service (`Lambda`)
*   **Permissions Policy**: `AmazonS3FullAccess`
*   **Role Name**: `LambdaS3CleanupRole`

### Step 3: Create the AWS Lambda Function
*   **Function Name**: `S3-Old-File-Cleanup`
*   **Runtime Workspace**: `Python 3.12`
*   **Execution Role**: `LambdaS3CleanupRole`

### Step 4: Write and Deploy the Code
Source code is located inside `assignment-2/s3_cleanup_lambda.py`. The script evaluates files using a `TESTING_MODE` toggle to immediately process elements and clean up older resources.

### Step 5: Manual Invocation & Verification
The function was manually triggered using an `S3Test` mock event profile. The runtime cleared out all old testing elements successfully.

---

## 🔒 Assignment 3: S3 Encryption Monitoring & Compliance Audit

Automated serverless governance worker built using Python and Boto3 to programmatically audit S3 buckets, inspect server-side encryption (SSE) configurations, and surface security compliance logs.

### Step 1: Target Storage Architecture
*   **Audited Target Resource**: Maps to the existing `cleanup-test-bench-nagin` object container workspace.
*   **Evaluation Parameters**: Verifies encryption settings against corporate infrastructure security benchmarks.

### Step 2: Lambda IAM Execution Configuration
*   **Trusted Identity Relationship**: AWS Service (`Lambda`)
*   **Permissions Baseline Context**: Uses scoped credentials to evaluate metadata blocks without exposing core bucket read structures (e.g., `s3:GetEncryptionConfiguration`).

---

## 💾 Assignment 4: Automated EBS Backup Manager

A Python Boto3 script designed to automate the creation, lifecycle retention management, and alerting of AWS EBS volume snapshots.

### Step 1: Automation & Script Setup
The core automation logic is written in Python using the Boto3 SDK inside `assignment-4/ebs_backup_manager.py`. The tool identifies target storage infrastructure using explicit resource resource tags.

### Step 2: Operational Workflow
1.  **Backup Creation**: Scans for active EBS volumes matching specific tag criteria (e.g., `Backup=True`) and initializes crash-consistent point-in-time snapshots.
2.  **Cost Optimization & Retention**: Inspects the creation timestamps of existing snapshots and automatically purges stale assets older than a designated retention threshold (e.g., 7 days) to minimize unnecessary AWS infrastructure spending.
3.  **Real-Time Alerts**: Transmits a summary execution report directly to a team chat platform via a Slack Webhook incoming endpoint upon completing the job.

### 📸 Verification and Tracking Screenshots

#### 1. Backup Creation Logs
*Description: Terminal output displaying the execution script successfully discovering target volumes and generating snapshots.*
![Backup Creation](./screenshots/01_backup_creation.png)

#### 2. Cost Optimization & Stale Cleanup
*Description: Validation showing the automated pruning module isolating and removing snapshots past their retention maturity.*
![Retention Cleanup](./screenshots/02_retention_deletion.png)

#### 3. Real-Time Alert Notification
*Description: Instant chat confirmation message delivered containing details of the backup cycle status.*
![Notification Alert](./screenshots/03_slack_notification.png)
