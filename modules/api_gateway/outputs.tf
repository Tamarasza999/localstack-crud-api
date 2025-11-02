output "api_id" { 
  value = aws_api_gateway_rest_api.main.id 
}

output "invoke_url" { 
  value = "http://localhost:5566/restapis/${aws_api_gateway_rest_api.main.id}/${var.env}/_user_request_/users"
}

output "base_url" {
  value = "http://localhost:5566/restapis/${aws_api_gateway_rest_api.main.id}/${var.env}/_user_request_"
}