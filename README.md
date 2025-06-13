# DataVault AWS Data Pipeline

A secure and scalable data processing pipeline built on AWS for enterprise data storage and processing.

## Architecture Overview

This project implements a fully managed, cost-effective data processing pipeline using AWS services:

- **Amazon S3**: Storage buckets for raw, processed, and archived data
- **AWS Lambda**: Serverless functions for data processing and transformation
- **Amazon Kinesis**: Real-time data ingestion and processing
- **Amazon Redshift**: Data warehousing for analytics
- **AWS IAM**: Security and access control
- **Amazon CloudWatch**: Monitoring and alerting

## Project Structure

```
.
├── .github/                    # GitHub related files
├── infrastructure/            # Terraform IaC files
│   ├── main.tf               # Main Terraform configuration
│   ├── variables.tf          # Terraform variables
│   └── outputs.tf            # Terraform outputs
├── src/                      # Source code
│   ├── processors/           # Data processing Lambda functions
│   ├── utils/               # Utility functions
│   └── tests/               # Test files
└── docs/                    # Documentation
```

## Prerequisites

- AWS CLI configured with appropriate credentials
- Python 3.8+
- Terraform
- Docker (optional, for local testing)

## Setup and Deployment

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd datavault-aws-pipeline
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Deploy infrastructure:

   ```bash
   cd infrastructure
   terraform init
   terraform apply
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS configuration
   ```

## Security

- All data is encrypted at rest using AWS KMS
- IAM roles follow the principle of least privilege
- Network access is restricted using Security Groups and NACLs
- Audit logging enabled for all critical operations

## Monitoring

The project includes CloudWatch Dashboards and Alerts for:

- Failed Lambda executions
- High latency in Kinesis processing
- S3 bucket operations
- Redshift query performance

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
