EXTERNAL_IP=$(kubectl get svc appapi-svc -n appapi --template="{{range .status.loadBalancer.ingress}}{{.ip}}{{end}}")
EXTERNAL_PORT=$(kubectl get svc appapi-svc -n appapi --template="{{range .spec.ports}}{{.port}}{{end}}")
curl http://${EXTERNAL_IP}:8080/appapi/state
