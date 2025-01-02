terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.digitalocean_token
}

resource "digitalocean_droplet" "docker_machine" {
  name   = "docker-droplet"
  region = var.region
  size   = var.size
  image  = var.image

  ssh_keys = [digitalocean_ssh_key.my_key.fingerprint]

  tags = var.tags
}

resource "digitalocean_ssh_key" "my_key" {
  name       = "joao_ocean"
  public_key = file("~/.ssh/joao_ocean_rsa.pub")
}

output "droplet_ip" {
  value = digitalocean_droplet.docker_machine.ipv4_address
}
