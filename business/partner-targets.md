 # partner-targets.md

## Partner Integration Roadmap for api-sentry

The following is a list of potential SaaS/API partners for api-sentry integration, prioritized by value-add, integration effort, and revenue-share opportunities.

### 1. GitHub ([API documentation](https://docs.github.com/en/rest))
- Free-tier limits: Unlimited public repositories, 3 private repositories
- Integration effort: Medium
- Value-add: Automatically create api-sentry alerts for GitHub projects, improving developer workflow and reducing response time to performance degradation.
- Rationale: GitHub is a popular platform for developers, making it an ideal partner for api-sentry to reach a wider audience and improve integration with existing developer workflows.

### 2. Slack ([API documentation](https://api.slack.com/))
- Free-tier limits: 10,000 messages per month, 10 integrations per workspace
- Integration effort: Medium
- Value-add: Send api-sentry alerts as Slack notifications, allowing developers to stay informed about performance issues without constantly checking the api-sentry dashboard.
- Rationale: Slack is a widely-used communication tool among developers, making it a natural choice for api-sentry to integrate with for real-time notifications.

### 3. AWS Lambda ([API documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html))
- Free-tier limits: 1M free requests per month, 400,000 GB-seconds of compute time per month
- Integration effort: Large
- Value-add: Integrate api-sentry with AWS Lambda functions to automatically trigger performance tests and alerts based on specific conditions or triggers.
- Rationale: AWS Lambda is a popular serverless computing service, and integrating api-sentry with Lambda functions can provide a powerful tool for developers to proactively monitor and optimize their applications.

### 4. New Relic ([API documentation](https://docs.newrelic.com/docs/apm/apm-api/))
- Free-tier limits: Limited to 100,000 transactions per month, 100,000 errors per month, and 100,000 custom events per month
- Integration effort: Large
- Value-add: Integrate api-sentry with New Relic's APM (Application Performance Monitoring) service to provide a more comprehensive view of application performance, including real-time monitoring, trend analysis, and root cause analysis.
- Rationale: New Relic is a well-established APM service, and integrating api-sentry with New Relic can provide a valuable addition to the api-sentry offering, offering developers a more complete solution for monitoring and optimizing their applications.

### 5. CircleCI ([API documentation](https://circleci.com/docs/api/))
- Free-tier limits: 100 builds per month, 10 concurrent builds
- Integration effort: Large
- Value-add: Integrate api-sentry with CircleCI to automatically trigger performance tests and alerts as part of the continuous integration/continuous deployment (CI/CD) pipeline.
- Rationale: CircleCI is a popular CI/CD service, and integrating api-sentry with CircleCI can provide a powerful tool for developers to ensure that their applications are performing optimally as part of the development and deployment process.

### 6. Datadog ([API documentation](https://docs.datadoghq.com/api/))
- Free-tier limits: Limited to 50,000 API calls per month, 100,000 metrics per month, and 100,000 events per month
- Integration effort: Large
- Value-add: Integrate api-sentry with Datadog's monitoring service to provide a more comprehensive view of application performance, including real-time monitoring, trend analysis, and root cause analysis.
- Rationale: Datadog is a well-established monitoring service, and integrating api-sentry with Datadog can provide a valuable addition to the api-sentry offering, offering developers a more complete solution for monitoring and optimizing their applications.

### 7. Sentry ([API documentation](https://docs.sentry.io/platforms/))
- Free-tier limits: Limited to 50,000 events per month, 5 projects, and 5 team members
- Integration effort: Large
- Value-add: Integrate api-sentry with Sentry's error tracking and monitoring service to provide a more comprehensive view of application performance, including real-time monitoring, trend analysis, and root cause analysis.
- Rationale: Sentry is a well-established error tracking and monitoring service, and integrating api-sentry with Sentry can provide a valuable addition to the api-sentry offering, offering developers a more complete solution for monitoring and optimizing their applications.