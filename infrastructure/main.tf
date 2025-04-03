# Main Terraform configuration file

provider "aws" {
  region = var.aws_region
}

# Create a random suffix for unique resource names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

locals {
  name_suffix = random_string.suffix.result
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# VPC and networking
module "networking" {
  source = "./modules/networking"

  vpc_name            = "${var.project_name}-vpc-${local.name_suffix}"
  vpc_cidr            = var.vpc_cidr
  availability_zones  = var.availability_zones
  private_subnet_cidr = var.private_subnet_cidr
  public_subnet_cidr  = var.public_subnet_cidr
  tags                = local.common_tags
}

# EKS cluster
module "eks" {
  source = "./modules/eks"

  cluster_name       = "${var.project_name}-eks-${local.name_suffix}"
  cluster_version    = var.eks_cluster_version
  vpc_id             = module.networking.vpc_id
  subnet_ids         = module.networking.private_subnet_ids
  node_group_name    = "${var.project_name}-node-group"
  node_instance_type = var.node_instance_type
  node_desired_size  = var.node_desired_size
  node_min_size      = var.node_min_size
  node_max_size      = var.node_max_size
  tags               = local.common_tags
}

# S3 bucket for static assets and backups
module "storage" {
  source = "./modules/storage"

  bucket_name = "${var.project_name}-storage-${local.name_suffix}"
  tags        = local.common_tags
}

# Output the cluster endpoint and other important information
output "eks_cluster_endpoint" {
  description = "The endpoint for the EKS cluster"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "The name of the EKS cluster"
  value       = module.eks.cluster_name
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = module.storage.bucket_name
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.networking.vpc_id
}

output "kubeconfig_command" {
  description = "Command to configure kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}