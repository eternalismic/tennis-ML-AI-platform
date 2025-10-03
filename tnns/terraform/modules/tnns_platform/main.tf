terraform {
  required_providers {
    helm = { source = "hashicorp/helm", version = "~> 2.12" }
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.29" }
  }
}
resource "kubernetes_namespace" "ns" {
  metadata { name = var.namespace }
}
resource "helm_release" "tnns" {
  name             = var.release_name
  repository       = ""
  chart            = var.chart_path
  namespace        = var.namespace
  create_namespace = false
  values           = [ yamlencode(var.values) ]
}
