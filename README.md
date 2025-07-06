# 📦 pipeline-anp-azure

> Azure Function que baixa planilhas históricas de preços de combustíveis da ANP e faz upload para um container no Azure Blob Storage.

---

## 📌 Visão Geral

Este projeto utiliza **Azure Functions** em Python para automatizar a coleta de arquivos públicos da ANP (Agência Nacional do Petróleo), salvando-os de forma organizada no Azure Blob Storage.

### Principais recursos

- ⏰ **Timer Trigger:** Executa automaticamente todos os dias no horário agendado.
- 🌐 **HTTP Trigger:** Permite execução manual via requisição HTTP.
- 🚀 **Deploy automatizado:** Workflow GitHub Actions pronto para CI/CD.

---

## 🧱 Estrutura do Projeto

```text
.
├── SerieHistoricaMunicipiosHttp/      # Function com HTTP Trigger
├── SerieHistoricaMunicipiosTimer/     # Function com Timer Trigger
├── requirements.txt                   # Dependências Python
├── host.json                          # Configuração da Function App
├── README.md                          # Documentação
└── .github/
    └── workflows/
        └── main_pipeline-anp.yml     # Pipeline CI/CD GitHub Actions
```

---

## 🔐 Variáveis de Ambiente Necessárias

As funções dependem das seguintes variáveis no App Service / Function App:

| Nome           | Descrição                                 |
|----------------|-------------------------------------------|
| BLOB_CONN_STR  | Connection string da conta Azure Blob Storage |

**Como obter:**
1. Acesse sua conta de armazenamento no portal do Azure.
2. Vá em **Chaves de acesso** e copie a string de conexão.
3. Adicione como variável de ambiente no Function App com o nome `BLOB_CONN_STR`.

---

## 📦 Dependências

Inclua no `requirements.txt`:

```text
azure-functions
azure-storage-blob
requests
beautifulsoup4
```

---

## ⏳ Agendamento da Função

A execução automática está definida para **06:00 UTC** diariamente.

> Para alterar o horário, edite o campo `schedule` em `function.json` da função Timer.

---

## ▶️ Uso

### ✅ Execução Automática (Timer Trigger)
A função será disparada diariamente, buscando os arquivos mais recentes da ANP e salvando no Blob Storage.

### 🔘 Execução Manual (HTTP Trigger)
Faça uma chamada HTTP para a função:

```bash
curl 'https://<function-app>.azurewebsites.net/api/SerieHistoricaMunicipiosHttp?code=<FUNCTION_KEY>'
```

**Exemplo de resposta JSON:**

```json
{
  "total_uploaded": 2,
  "details": [
    {"file": "mensal-municipios-202406.xlsx", "status": "uploaded", "size_bytes": 123456},
    {"file": "mensal-municipios-202405.xlsx", "status": "uploaded", "size_bytes": 120000}
  ]
}
```

---

## 🚀 Deploy Automático com GitHub Actions

O deploy acontece automaticamente ao fazer push na branch `main`.


---

## ✅ Passos de Configuração

1. **Configure os segredos no repositório GitHub:**
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`

2. **Crie as federated credentials no Microsoft Entra ID (Azure AD).**

3. **Certifique-se de que:**
   - O Function App já está criado.
   - O Blob Storage está configurado.

4. **Deploy automático:**
   - A cada novo push, o GitHub Actions fará o deploy automaticamente.

---

## 🧪 Observações

- O projeto está pronto para uso em produção.
- Logs podem ser acessados via Kudu ou Application Insights.
- Para alterar o container ou caminho no Blob, modifique as constantes no `__init__.py`.

---

## 🤝 Contribuições

Contribuições são bem-vindas!

Abra uma *Issue* ou *Pull Request* com sugestões, bugs ou melhorias.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais informações.