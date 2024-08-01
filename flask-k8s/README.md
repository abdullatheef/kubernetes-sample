eval $(minikube docker-env)
docker build -t flask-app .




kubectl get secret --namespace monitoring loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo



p3NMgFFCqhFMhezNCIpJUlNZh9CbW5iJqN7ETn77

AKIA6GBME52T44EKZGEO
tJOAzW8HqaS8xSehf/HURbkGWVvv8slcV+0lvdYs




grafana/loki-stack
>
helm show values grafana/loki-stack > values.yaml 
>
edit grafana:true, image: latest
>
helm install --values values.yaml loki grafana/loki-stack -n monitoring
>
grafana data source --> http://loki:3100




helm show values prometheus-community/kube-prometheus-stack > prometheus_values.yaml
>
edit grafana:false
>
helm install --values prometheus_values.yaml prometheus prometheus-community/kube-prometheus-stack -n monitoring
>
grafana data source --> http://prometheus-operated.monitoring.svc.cluster.local:9090



in the prometheus_values.yaml
    additionalScrapeConfigs: |
      - job_name: 'flask-app-metrics'
        static_configs:
          - targets: ['http://flask-app-service.myns.svc.cluster.local']
        metrics_path: /metrics
        scrape_interval: 30s

helm upgrade prometheus prometheus-community/kube-prometheus-stack -f prometheus_values.yaml -n monitoring



To store s3 logs, in values yaml


loki:
  enabled: true
  isDefault: true
  url: http://{{(include "loki.serviceName" .)}}:{{ .Values.loki.service.port }}
  readinessProbe:
    httpGet:
      path: /ready
      port: http-metrics
    initialDelaySeconds: 45
  livenessProbe:
    httpGet:
      path: /ready
      port: http-metrics
    initialDelaySeconds: 45
  datasource:
    jsonData: "{}"
    uid: ""
#TOADD
  env:

  config:
    schema_config:
      configs:
        - from: 2021-05-12
          store: boltdb-shipper
          object_store: s3
          schema: v11
          index:
            prefix: loki_index_
            period: 24h
    storage_config:
      aws:
        s3: s3://ap-south-1/itzmeontv-public
        #s3forcepathstyle: true
        bucketnames: itzmeontv-public
        region: ap-south-1
        insecure: false
        sse_encryption: false
      boltdb_shipper:
        shared_store: s3
        cache_ttl: 24h



VMAGENT issue
------------	
helm list -A
helm upgrade vmagent vm/victoria-metrics-agent --version 0.7.20 -n monitoring
