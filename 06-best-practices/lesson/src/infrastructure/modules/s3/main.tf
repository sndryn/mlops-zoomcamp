resource "aws_s3_bucket" "s3_bucket" {
    bucket  = var.bucket_name
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.s3_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "name" {
    value = aws_s3_bucket.s3_bucket.bucket
}
