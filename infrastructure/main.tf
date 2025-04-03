provider "aws" {
  region = var.aws_region
}

module "network" {
  source = "./modules/network"
  
  vpc_cidr        = var.vpc_cidr
  cluster_name    = var.cluster_name
  aws_region      = var.aws_region
}

module "eks" {
  source = "./modules/eks"
  
  cluster_name    = var.cluster_name
  vpc_id          = module.network.vpc_id
  subnet_ids      = module.network.subnet_ids
  node_group_name = "${var.cluster_name}-node-group"
  instance_types  = var.instance_types
  desired_size    = var.desired_size
  min_size        = var.min_size
  max_size        = var.max_size
}

module "storage" {
  source = "./modules/storage"
  
  bucket_name     = "${var.cluster_name}-artifacts"
  aws_region      = var.aws_region
}

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = var.cluster_name
}

output "s3_bucket_name" {
  description = "S3 bucket for artifacts"
  value       = module.storage.bucket_name
}
