# pipeline-anp-azure

Azure Function that downloads historical fuel price spreadsheets from ANP and
uploads them to an Azure Blob Storage container.

## Usage

The function executes automatically every day at 06:00 (UTC) using a timer
trigger. To trigger it manually, send an HTTP `GET` or `POST` request to the
function's URL:

```bash
curl https://<function-app>.azurewebsites.net/api/SerieHistoricaMunicipios
```

On manual invocation the function responds with a JSON summary of uploaded
files. When triggered by the schedule no response body is produced.
