provider "aws" {
    region = var.aws_region
}

resource "aws_instance" "discord_bot" {
    ami             = var.ami_id
    instance_type   = var.instance_type

    key_name        = aws_key_pair.generated_key.key_name

    security_groups = [aws_security_group.sg_ssh.name]

    user_data = templatefile("user_data.sh.tpl", {
        python_script = file("${path.module}/Code/bot.py"),
        requirements  = file("${path.module}/Code/requirements.txt"),
        env_file      = file("${path.module}/Code/.env")
    })

    tags = {
        Name = var.instance_name
    }
}

resource "aws_security_group" "sg_ssh" {
    name        = "allow_ssh"
    description = "Allow SSH inbound traffic"

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = [var.trusted_ip]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_key_pair" "generated_key" {
  key_name = "generated-key"
  public_key = file(var.public_key_path)
}