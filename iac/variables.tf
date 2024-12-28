variable "digitalocean_token" {
  description = "Token de autenticação na DigitalOcean"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "Região do droplet"
  type        = string
  default     = "nyc3"
}

variable "size" {
  description = "Tamanho da máquina"
  type        = string
  default     = "s-1vcpu-1gb"
}

variable "image" {
  description = "Imagem do sistema operacional com Docker"
  type        = string
  default     = "docker-20-04"
}

variable "tags" {
  description = "Tags para o droplet"
  type        = list(string)
  default     = ["docker"]
}
