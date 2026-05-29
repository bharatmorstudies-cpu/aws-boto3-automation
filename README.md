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

## 📸 Deployment Screenshots

### EC2 Dashboard Setup
Below is the verification screenshot showing both target EC2 instances in their correct initial states before running the automation script.

![EC2 Setup Verification](./screenshots/ec2_setup.png)
