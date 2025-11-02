resource "aws_dynamodb_table" "main" {
  name         = "${var.env}-${var.table_name}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "userId"

  attribute {
    name = "userId"
    type = "S"
  }

  tags = {
    Environment = var.env
    Name        = "${var.env}-${var.table_name}"
  }
}
