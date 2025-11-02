terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  backend "local" { path = "terraform.tfstate" }
}

provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    iam        = "http://localhost:4566"
    lambda     = "http://localhost:4566"
    apigateway = "http://localhost:4566"
    dynamodb   = "http://localhost:4566"
  }
}

module "database" {
  source     = "../../modules/dynamodb"
  env        = var.env
  table_name = "users"
}

module "api_lambda" {
  source        = "../../modules/lambda"
  env           = var.env
  function_name = "users-api"
  runtime       = "python3.9"
}

module "api_gateway" {
  source           = "../../modules/api_gateway"
  env              = var.env
  lambda_invoke_arn = module.api_lambda.invoke_arn
}
