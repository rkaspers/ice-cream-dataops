# CDF Bootcamp - Ice Cream Factory DataOps Solution

This repository contains the complete solution for the **Cognite Data Fusion (CDF) Bootcamp**, implementing a full DataOps pipeline for the Ice Cream Factory use case.


## 📋 Overview

This project demonstrates a production-ready DataOps implementation using the **Cognite Toolkit** to manage and deploy resources to Cognite Data Fusion. The solution ingests data from the Ice Cream Factory API, transforms it, and calculates OEE (Overall Equipment Effectiveness) metrics.

## 🏗️ Architecture

The solution implements a complete data pipeline with the following components:

### Data Flow
```
Ice Cream Factory API
    ↓
Hosted Extractors (Assets & Time Series)
    ↓
RAW Tables
    ↓
Transformations (Asset Hierarchy & Contextualization)
    ↓
Data Model Instances
    ↓
Functions (Datapoints Extraction & OEE Calculation)
    ↓
Analytics & Insights
```

### Workflow Pipeline

The automated workflow (`wf_icapi_data_pipeline`) orchestrates the entire data pipeline:

1. **create_asset_hierarchy** - Transformation that creates asset hierarchy from RAW data
2. **contextualize_ts_assets** - Transformation that links time series to assets
3. **icapi_datapoints_extractor** - Function that extracts datapoints from the API
4. **oee_timeseries** - Function that calculates OEE metrics

## 📁 Project Structure

```
workspace/
├── cdf.toml                          # Cognite Toolkit configuration
├── ice-cream-dataops/                # Main organization directory
│   ├── config.test.yaml              # Test environment configuration
│   ├── config.prod.yaml              # Production environment configuration
│   └── modules/
│       └── bootcamp/
│           ├── data_foundation/      # Base IAM and permissions
│           │   └── auth/
│           │       └── data_developer.Group.yaml
│           ├── ice_cream_api/        # Ice Cream Factory integration
│           │   ├── auth/
│           │   │   └── icapi_extractors.Group.yaml
│           │   ├── data_models/
│           │   │   └── ice_cream_data_model.space.yaml
│           │   ├── data_sets/
│           │   │   └── data_sets.DataSet.yaml
│           │   ├── functions/
│           │   │   └── icapi_datapoints_extractor/
│           │   │       ├── handler.py
│           │   │       ├── ice_cream_factory_api.py
│           │   │       └── requirements.txt
│           │   ├── hosted_extractors/
│           │   │   └── Ice Cream Factory API/
│           │   │       ├── assets/
│           │   │       ├── timeseries/
│           │   │       └── Source.yaml
│           │   ├── raw/
│           │   │   └── ice-cream-factory-db.Table.yaml
│           │   ├── transformations/
│           │   │   ├── create_asset_hierarchy.Transformation.yaml
│           │   │   ├── create_asset_hierarchy.Transformation.sql
│           │   │   └── create_asset_hierarchy.schedule.yaml
│           │   ├── workflows/
│           │   │   ├── wf_icapi_data_pipeline.Workflow.yaml
│           │   │   ├── wf_icapi_data_pipeline.WorkflowVersion.yaml
│           │   │   └── wf_icapi_data_pipeline.WorkflowTrigger.yaml
│           │   └── module.toml
│           └── use_cases/
│               └── oee/              # OEE calculation use case
│                   ├── auth/
│                   │   └── data_pipeline_oee.Group.yaml
│                   ├── data_models/
│                   │   └── oee_timeseries.space.yaml
│                   ├── data_sets/
│                   │   └── data_sets.DataSet.yaml
│                   ├── functions/
│                   │   └── oee_timeseries/
│                   │       ├── handler.py
│                   │       └── requirements.txt
│                   └── module.toml
└── .github/
    └── workflows/
        └── deploy.yaml               # GitHub Actions CI/CD pipeline
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Access to a CDF project (e.g., `cdf-bootcamp-73-test`)
- Azure AD application with appropriate permissions
- Cognite Toolkit CLI installed (`pip install cognite-toolkit`)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bootcamp/workspace
   ```

2. **Install dependencies**
   ```bash
   pip install cognite-toolkit
   ```

3. **Set up environment variables**

   Create a `.env` file in the `ice-cream-dataops/` directory:
   ```bash
   # CDF Project Configuration
   CDF_PROJECT=cdf-bootcamp-73-test
   CDF_CLUSTER=westeurope-1
   
   # Azure AD Configuration
   IDP_TENANT_ID=<your-tenant-id>
   IDP_CLIENT_ID=<your-client-id>
   IDP_CLIENT_SECRET=<your-client-secret>
   IDP_TOKEN_URL=https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token
   IDP_SCOPES=https://<cluster>.cognitedata.com/.default
   
   # Extractor Credentials
   ICAPI_EXTRACTORS_CLIENT_ID=<extractor-client-id>
   ICAPI_EXTRACTORS_CLIENT_SECRET=<extractor-client-secret>
   
   # OEE Pipeline Credentials
   DATA_PIPELINE_OEE_CLIENT_ID=<oee-client-id>
   DATA_PIPELINE_OEE_CLIENT_SECRET=<oee-client-secret>
   ```

### Deployment

1. **Build the configuration**
   ```bash
   cd workspace
   cdf build
   ```

2. **Deploy to CDF (dry-run)**
   ```bash
   cdf deploy --dry-run
   ```

3. **Deploy to CDF**
   ```bash
   cdf deploy
   ```

## 🔧 Key Components

### Hosted Extractors

Two hosted extractors pull data from the Ice Cream Factory API:

- **Assets Extractor**: Fetches asset data daily and stores it in RAW
- **Time Series Extractor**: Fetches time series metadata hourly

### Transformations

- **create_asset_hierarchy**: Creates a structured asset hierarchy in CDF from RAW data
  - Scheduled to run daily at 01:13 AM
  - Transforms flat RAW data into hierarchical asset structure

- **contextualize_ts_assets**: Links time series to their corresponding assets
  - Uses matching logic to associate data streams with equipment

### Functions

- **icapi_datapoints_extractor**: Extracts historical datapoints from the API
  - Configurable time window (default: 1 hour)
  - Writes data to CDF time series

- **oee_timeseries**: Calculates OEE metrics
  - Availability, Performance, Quality, and Overall OEE
  - Processes data from multiple production lines

### Workflows

The `wf_icapi_data_pipeline` workflow orchestrates the entire pipeline:
- Ensures proper execution order with dependencies
- Includes retry logic (3 retries per task)
- Aborts on failure to maintain data consistency
- Can be triggered manually or on a schedule

## 🔐 Security & Permissions

The solution implements least-privilege access control with three IAM groups:

1. **data_developer**: Full administrative access for development
2. **icapi_extractors**: Permissions for ingesting and transforming data
3. **data_pipeline_oee**: Permissions for OEE calculations

Each group has precisely scoped capabilities to specific datasets and spaces.

## 📊 Data Models

- **Ice Cream Factory Data Model** (`icapi_dm_space`): Contains assets and time series
- **OEE Time Series** (`oee_ts_space`): Contains calculated OEE metrics

## 🔄 CI/CD Pipeline

The repository includes GitHub Actions workflow for automated deployment:
- Validates configuration on pull requests
- Automatically deploys to test/prod environments on merge
- Located in `.github/workflows/deploy.yaml`

## 📚 Learning Outcomes

This bootcamp solution demonstrates:

- ✅ Infrastructure as Code (IaC) with Cognite Toolkit
- ✅ Data ingestion using Hosted Extractors
- ✅ Data transformation with CDF Transformations
- ✅ Serverless computing with CDF Functions
- ✅ Workflow orchestration
- ✅ IAM and security best practices
- ✅ CI/CD automation with GitHub Actions
- ✅ Data model design and implementation

## 🛠️ Troubleshooting

### Check Group Permissions

A utility script is provided to verify IAM group permissions:

```bash
cd ice-cream-dataops
python3 check_group_permissions.py
```

This will display all capabilities for the `icapi_extractors` group and verify required permissions.

### Common Issues

1. **403 Forbidden errors**: Check that IAM groups have proper permissions
2. **Transformation failures**: Verify RAW data exists and is properly formatted
3. **Function timeouts**: Adjust timeout values in workflow definition
4. **Hosted extractor errors**: Verify API connectivity and credentials

## 📖 Resources

- [Cognite Toolkit Documentation](https://developer.cognite.com/sdks/toolkit/)
- [CDF Bootcamp Materials](https://docs.cdf-bootcamp.cogniteapp.com/)
- [Cognite Python SDK](https://cognite-sdk-python.readthedocs-hosted.com/)

## 👥 Contributing

This is a bootcamp solution repository. For improvements or questions:
1. Create an issue describing the problem or enhancement
2. Submit a pull request with proposed changes
3. Ensure all tests pass and configuration validates

## 📝 License

This project is part of the Cognite Data Fusion Bootcamp training materials.

---

**Project**: cdf-bootcamp-73-test  
**Environment**: Test/Production  
**Toolkit Version**: 0.6.19

