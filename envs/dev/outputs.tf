output "api_url" { value = module.api_gateway.invoke_url }
output "lambda_arn" { value = module.api_lambda.function_arn }
output "dynamodb_table" { value = module.database.table_name }
