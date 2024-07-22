# Minio
## Local Compatible S3 Storage

### Description

MinIO is a high-performance, S3 compatible object store. It is built for large scale AI/ML, data lake and database workloads. It is software-defined and runs on any cloud or on-premises infrastructure. MinIO is dual-licensed under open source GNU AGPL v3 and a commercial enterprise license.

This project uses Minio to store and retrieve data from a bucket-like storage, which is compatible with AWS S3 protocol.

### Use

For this project, once the **Video Stream Processor** detects frames were there is movements the images will be stored in a bucket-like format in the Minio storage. This will allow the user to retrieve the images from the storage and use them for further analysis (either by person or tools) or to store them for future reference.

With the Minio storage, the user will be able to use the project completelly locally or set it up so it works with the cloud, depending on the user's needs and availability of resources and context of use. In this way, it expands the possibilities of use for the project making it more versatile and adaptable to different scenarios.

### Installation and Use

#### Local use

In order to use Minio locally, the user must have the Docker service installed and running on the machine. If you don't have Docker installed, you can download it from the [official website](https://docs.docker.com/get-docker/).

After installing Docker, the user can run the following command to start the Minio service through a compose:

```bash
# Run from the docker/minio directory
docker-compose up -d
```

This command will start the Minio service on the port `9000` or `9001`. To access the Minio dashboard, open your browser and go to one of those URLs in localhost.

### Execution

Once the Docker service is running, the user can access the Minio dashboard by opening the proper URL in the browser. There, all of the own Minio buckets and configurations can be managed. 

It is important that the user configures the Minio service with the proper credentials and configurations in order to use it properly: 

1. In the `docker-compose.yml` file, the user can set the `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` environment variables to the desired values which configures the access variables for the Minio service per se. The first time the minio service is started it will use these variables to create access rights that later will be used to be able to access the dashboard and managed buckets.
2. Bucket credentials for the file uploader. It will be needed `access_key` and `secret_key` to be able to upload files to the bucket. These credentials can be set in the `config/processor/variables.yaml` file.

### AWS Interusability

Initially only the variables are necessary for connecting to the Minio service, more information about configuration can be obtained in the [Official Minio Documentation (AWS Secret Manager)](https://min.io/docs/kes/integrations/aws-secrets-manager/).

### API Reference

All of the API references for the **python package** we are using in this project can be found in the [official Minio documentation](https://min.io/docs/minio/linux/developers/python/API.html).
