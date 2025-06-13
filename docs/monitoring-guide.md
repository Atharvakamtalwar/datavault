# Monitoring and Alerting Guide

## Infrastructure Monitoring

### Prometheus Setup

1. **Installation**
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

2. **Key Metrics**
- `datavault_processing_latency_seconds`: Processing time for each record
- `datavault_records_processed_total`: Total number of records processed
- `datavault_processing_errors_total`: Total number of processing errors
- `datavault_s3_operations_total`: S3 operation counts
- `datavault_kinesis_lag_records`: Kinesis processing lag

3. **Alert Rules**
```yaml
groups:
- name: datavault
  rules:
  - alert: HighProcessingLatency
    expr: datavault_processing_latency_seconds > 30
    labels:
      severity: warning
  - alert: HighErrorRate
    expr: rate(datavault_processing_errors_total[5m]) > 0.1
    labels:
      severity: critical
```

### Grafana Dashboards

1. **Main Dashboard Panels**
- Processing Pipeline Overview
- Error Rates and Latencies
- Resource Utilization
- Cost Metrics

2. **Data Source Configuration**
- Prometheus
- CloudWatch
- AWS X-Ray

3. **Alert Notifications**
- Email Integration
- Slack Notifications
- PagerDuty Integration

## Application Monitoring

### Lambda Function Monitoring
1. **CloudWatch Metrics**
- Invocation count
- Error count
- Duration
- Memory usage
- Throttling

2. **Custom Metrics**
- Records processed
- Validation errors
- Data quality metrics
- Business KPIs

### Kinesis Stream Monitoring
1. **Performance Metrics**
- Iterator Age
- Put/Get Records Latency
- Throughput
- Error rates

2. **Shard Metrics**
- Shard count
- Records per shard
- Bytes per shard

## Cost Monitoring

### AWS Cost Explorer Integration
1. **Resource Tags**
- Environment
- Component
- Team
- Project

2. **Cost Metrics**
- Daily processing costs
- Storage costs
- Network transfer costs
- Lambda execution costs

## Troubleshooting Guide

### Common Issues

1. **High Processing Latency**
```sql
SELECT
  timestamp,
  latency,
  error_type,
  record_count
FROM processing_metrics
WHERE latency > 30
ORDER BY timestamp DESC
LIMIT 10;
```

2. **Data Quality Issues**
```python
def validate_data_quality(records):
    issues = []
    for record in records:
        if not record.get('customer_id'):
            issues.append({
                'type': 'missing_field',
                'field': 'customer_id',
                'record_id': record.get('id')
            })
    return issues
```

3. **Pipeline Failures**
- Check CloudWatch Logs
- Verify IAM permissions
- Review network connectivity
- Check resource limits

### Recovery Procedures

1. **Data Recovery**
```bash
# Restore data from backup
aws s3 cp s3://backup-bucket/backup.zip s3://raw-data-bucket/

# Reprocess failed records
python src/processors/retry_failed.py --date 2025-06-13
```

2. **Service Recovery**
```bash
# Scale up resources
kubectl scale deployment datavault-processor --replicas=5

# Check service health
kubectl get pods -n datavault -o wide
```

## Best Practices

1. **Monitoring Strategy**
- Set realistic thresholds
- Implement gradual alerts
- Use correlation rules
- Regular review and updates

2. **Alert Management**
- Define severity levels
- Set up escalation paths
- Document response procedures
- Regular testing of alerts

3. **Dashboard Organization**
- Hierarchical view
- Business metrics first
- Technical details on demand
- Clear visualization
