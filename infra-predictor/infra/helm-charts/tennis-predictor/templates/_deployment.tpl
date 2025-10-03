{{- define "tennis-predictor.deployment" -}}
apiVersion: apps/v1
kind: Deployment
metadata: { name: tennis-predictor, labels: { app: tennis-predictor } }
spec:
  replicas: {{ .Values.replicaCount }}
  selector: { matchLabels: { app: tennis-predictor } }
  template:
    metadata: { labels: { app: tennis-predictor } }
    spec:
      containers:
        - name: app
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports: [ { containerPort: {{ .Values.service.port }} } ]
          env: {{- toYaml .Values.env | nindent 12 }}
{{- end -}}
