# BadlyWrittenWebapp-TempClipboard-

## Overview
This project is a simple web application that can be deployed on a single web server. The deployment process is straightforward, but there are a few important steps to follow to ensure everything runs smoothly.

## Prerequisites

- Amazon EC2 instance running **Amazon Linux** (other operating systems may cause issues with the deployment script).
- Access to a **database** and **S3 bucket** for the application to work correctly.
  
## Deployment Instructions

### 1. EC2 Instance Setup
To deploy the application, you need an EC2 instance running Amazon Linux. The deployment script is designed to work on Amazon Linux and may not work on other operating systems.

### 2. User Data Configuration
In the EC2 instance setup, you need to ensure that the deployment script is executed during the instance startup.

- Copy the contents of the `deployment.sh` script.
- Go to the **Advanced Settings** section in the EC2 launch configuration.
- Paste the `deployment.sh` script into the **User Data** field. This will ensure the script is executed automatically when the EC2 instance starts.

### 3. Database and Bucket Access
Make sure your EC2 instance is able to connect to both the database and the S3 bucket. This may require configuring IAM roles, security groups, and VPC settings to allow proper access.

## Usage
Once the EC2 instance is up and running, the web application will be deployed automatically. It’s a simple web app, and you can access it by visiting the public IP address or domain name of your EC2 instance.

## Notes
- Ensure the EC2 instance has proper IAM roles to access the database and S3 bucket.
