# Projeto Terraform para Provisionamento de Infraestrutura do Bot de WhatsApp

![Terraform Logo](https://www.terraform.io/assets/images/og-image-8b3e4f7d.png)

Este diretório **`iac`** (“Infraestrutura como Código”) é parte do projeto do **Bot de WhatsApp** e tem como objetivo provisionar automaticamente a infraestrutura necessária para hospedar o bot na DigitalOcean. Utilizamos **Terraform** para gerenciar a infraestrutura de maneira declarativa e automatizada.

## 🚀 Estrutura de Arquivos

O diretório `iac` está organizado nos seguintes arquivos:

### 📂 1. `main.tf`

Arquivo principal que define os recursos de infraestrutura para o bot. Ele:

- Configura o **provider** da DigitalOcean usando o token de API.
- Provisiona um **droplet** que serve como servidor do bot.
- Configura a chave SSH para acesso seguro ao servidor.
- Define os **outputs**, como o IP do servidor provisionado, para uso no deploy do bot.

### 📂 2. `variables.tf`

Declaração das variáveis utilizadas no projeto para facilitar a parametrização e reutilização do código. As variáveis incluem:

- `digitalocean_token`: Token de autenticação da API da DigitalOcean.
- `region`: Região do droplet.
- `size`: Configuração de recursos do droplet.
- `image`: Imagem usada no droplet (por padrão, Ubuntu 20.04 com Docker).
- `tags`: Tags para organização do recurso.

### 📂 3. `terraform.tfvars`

Arquivo que armazena os valores das variáveis declaradas em `variables.tf`. Este arquivo é usado para personalizar o provisionamento do droplet sem alterar os arquivos principais. **Importante**: Este arquivo é sensível e não deve ser incluído no repositório.

Exemplo:

```hcl
digitalocean_token = "seu_token_aqui"
region             = "nyc3"
size               = "s-1vcpu-1gb"
image              = "docker-20-04"
tags               = ["bot", "whatsapp"]
```

### 📂 4. `outputs.tf`

Arquivo que define os valores de saída exibidos após a execução do Terraform. Neste projeto, o principal output é o IP do droplet, que será usado para configurar e fazer o deploy do bot.

### 📂 5. `ssh_key.pub`

Chave pública SSH usada para acessar o droplet de forma segura. Certifique-se de que o arquivo corresponde à chave privada configurada no seu ambiente local.

## 🛠️ Fluxo de Trabalho

1. **Inicialize o Terraform:**

   ```bash
   terraform init
   ```

2. **Planeje o provisionamento:**

   ```bash
   terraform plan
   ```

   Verifique os recursos que serão criados.

3. **Aplique o provisionamento:**

   ```bash
   terraform apply
   ```

   Confirme a execução. Ao final, o IP do droplet será exibido.

4. **Acesse o servidor:**
   Use o IP exibido para acessar o servidor via SSH:

   ```bash
   ssh root@<ip_publico>
   ```

5. **Configure o bot no servidor:**
   Com o servidor provisionado, você pode configurar o bot usando ferramentas como Docker ou Ansible para realizar o deploy.

## 🤖 Integração com o Bot de WhatsApp

O servidor provisionado será usado para hospedar o backend do bot de WhatsApp. Você pode usar scripts adicionais ou playbooks Ansible para configurar dependências necessárias (ex.: Docker, Node.js, Python, etc.) diretamente no droplet.

### Exemplo de Deploy com Ansible

Crie um inventário dinâmico com o IP do droplet provisionado:

#### Arquivo `inventory.ini`

```ini
[bot_server]
<ip_publico> ansible_user=root ansible_ssh_private_key_file=~/.ssh/sua_chave_privada
```

Execute o playbook Ansible para configurar o ambiente do bot:

```bash
ansible-playbook -i inventory.ini deploy_bot.yml
```

## ✅ Boas Práticas

- **Gerenciamento de Tokens:** Nunca inclua o arquivo `terraform.tfvars` no repositório. Use um gerenciador de segredos como HashiCorp Vault ou GitHub Secrets.
- **Segurança SSH:** Verifique as permissões da chave privada para garantir o acesso seguro ao servidor.
- **Escalabilidade:** Adicione mais recursos, como balanceadores de carga ou volumes, conforme as necessidades do bot crescem.

## 🙌 Contribuições

Contribuições para melhorar a infraestrutura ou o processo de deploy são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

---

**Happy Terraforming!** 🌍
