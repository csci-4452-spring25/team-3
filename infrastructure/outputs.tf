output "instance_ip" {
    description = "Public IP of EC2 instance"
    value = aws_instance.discord_bot.public_ip
}