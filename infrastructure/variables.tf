variable "aws_region" {
    description = "AWS region to deploy to"
    default = "us-east-1"
}

variable "ami_id" {
    description = "AMI ID for EC2 instance"
    default = "ami-0c02fb55956c7d316"   # Ubuntu 22.04 LTS in us-east-1
}

variable "instance_type" {
    description = "The instance type for the EC2 instance"
    default = "t2.micro"
}

variable "trusted_ip" {
    description = "The IP address allowed to SSH into the instance"
    type = string  # WARNING: "0.0.0.0/0" allows SSH from any IP. restrict!!
}

variable "public_key_path" {
    description = "Path to SSH public key"
    type = string

}

variable "instance_name" {
    description = "Name of the EC2 instance"
    default = "Discord-Bot-Instance"
}