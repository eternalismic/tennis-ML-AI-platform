terraform {
  required_version = ">= 1.3.0"
  required_providers { google = { source = "hashicorp/google", version = "~> 5.0" } }
}
provider "google" { project = var.project, region = var.region }

resource "google_project_service" "services" {
  for_each = toset(["compute.googleapis.com","iam.googleapis.com","dns.googleapis.com","cloudresourcemanager.googleapis.com","storage.googleapis.com"])
  project = var.project
  service = each.key
}

resource "google_compute_network" "okd" { name = "${var.name}-net"; auto_create_subnetworks = false }
resource "google_compute_subnetwork" "okd" { name="${var.name}-subnet"; ip_cidr_range=var.cidr; region=var.region; network=google_compute_network.okd.id }

resource "google_compute_firewall" "allow_internal" { name="${var.name}-allow-internal"; network=google_compute_network.okd.self_link
  allows { protocol="tcp"; ports=["0-65535"] }
  allows { protocol="udp"; ports=["0-65535"] }
  source_ranges=[var.cidr]
}
resource "google_compute_firewall" "allow_external_api" { name="${var.name}-allow-api"; network=google_compute_network.okd.self_link
  allows { protocol="tcp"; ports=["6443","22623"] } source_ranges=["0.0.0.0/0"]
}
resource "google_compute_firewall" "allow_ingress" { name="${var.name}-allow-ingress"; network=google_compute_network.okd.self_link
  allows { protocol="tcp"; ports=["80","443"] } source_ranges=["0.0.0.0/0"]
}

resource "google_dns_managed_zone" "base" { name="${var.name}-zone"; dns_name="${var.base_domain}."; visibility="public" }
resource "google_storage_bucket" "state" { name="${var.project}-${var.name}-state"; location=var.region; force_destroy=true; uniform_bucket_level_access=true }

output "network" { value = google_compute_network.okd.name }
output "subnet"  { value = google_compute_subnetwork.okd.name }
output "zone"    { value = google_dns_managed_zone.base.name }
output "bucket"  { value = google_storage_bucket.state.name }
