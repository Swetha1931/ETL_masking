# ETL_masking
This project reads JSON data containing user login behavior from an AWS SQS Queue, masks personal identifiable information (PII), and writes the resulting records to a Postgres database.

## Prerequisites
1. Docker 
2. Docker-compose 
3. AWS CLI Local (pip install awscli-local)
4. Psql

## Code Execution
1. Clone this repository 
2. Run docker-compose up to start the test environment.
   ```
   docker-compose -f docker-compose.yml up -d --build
   ``` 
3. Testing local access of queue using AWS CLI Local:
   ```
   awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
   ```

5. Connect to a Postgres database and verify the table
   ```
   psql -d postgres -U postgres -p 5432 -h localhost -W
   ```
   ```
   SELECT * FROM user_logins;
   ```
## Decisions: 
1. How will you read messages from the queue?
> Using the read_messages_from_sqs() function to fetch messages, we can read the AWS SQS queue

2. What type of data structures should be used?
> Data class 'records' are the main type of data structure to represent the data

3. How will you mask the PII data so that duplicate values can be identified?
> Using the SHA algorithm, the same output (masked PII data) will be generated for the same input. Hence, duplicate values will generate the same SHA which can be used for the identification
    
4. What will be your strategy for connecting and writing to Postgres?
> The application uses the psycopg2 library to connect to the Postgres database

5. Where and how will your application run?
> By leveraging Docker, the application is portable, scalable, and can be deployed efficiently by containerization

### Deploy in production
- Use a containerization platform like Docker to package the application and Kubernetes for container orchestration
- Build docker images and push them into secure registry like AWS ECR

### Other components to make this production ready
- Implement monitoring and logging using tools like Prometheus and Grafana
- Set up a CI/CD pipeline like GitLab for deploying updates

### Scale with a growing dataset
- Use a scalable database solution like Apache Kafka or Kinesis for data streaming and increasing data volumes
Implement parallel processing using multiple workers to process messages concurrently
PII Recovery

### How can PII be recovered later on?
- Using tokenization, to map the original unmasked data with the masked SHA encrypted data, we can recover the PII later on
- The usage of SHA prevents reversal or decryption of the masked data but they can be stored in a secure AWS registry, with authorized access
- Implement access controls and auditing to ensure secure access to PII data

### Assumptions: 
- The SQS queue contains messages in JSON format with the required fields and consistent structure throughout the records
- The application has the necessary dependencies and libraries installed
- SHA encryption cannot be reversed
- PostgreSQL database is set up with the required table schema
  

 


