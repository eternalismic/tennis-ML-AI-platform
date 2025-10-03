variable "name"    { type = string default = "odh-okd" }
variable "project" { type = string }
variable "region"  { type = string default = "europe-west3" }
variable "cidr"    { type = string default = "10.60.0.0/16" }
variable "base_domain" { type = string default = "example.yourdomain.com" }
