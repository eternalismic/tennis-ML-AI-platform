provider "kubernetes" { config_path = pathexpand("~/.kube/config") }
provider "helm" { kubernetes { config_path = pathexpand("~/.kube/config") } }

module "tnns" {
  source       = "../modules/tnns_platform"
  namespace    = "tnns-dev"
  release_name = "tnns"
  chart_path   = "../../charts/tnns-cmpt-pwr"
  values = { kafka = { bootstrap = "my-cluster-kafka-bootstrap.kafka:9092" } }
}
