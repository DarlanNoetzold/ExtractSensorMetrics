import requests
import csv
from datetime import datetime

# Configurações
METRICS_URL = "http://server:8082/metrics"  # URL do endpoint do controller de métricas
CSV_FILE_PATH = f"/app/shared/metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"  # Nome do arquivo CSV com timestamp

def fetch_metrics():
    """Consulta as métricas no endpoint especificado e retorna os dados como JSON."""
    try:
        response = requests.get(METRICS_URL)
        response.raise_for_status()  # Levanta exceção para códigos de status HTTP de erro
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar as métricas: {e}")
        return None


def write_metrics_to_csv(metrics_data):
    """Escreve os dados de métricas em um arquivo CSV."""
    if not metrics_data:
        print("Nenhuma métrica para escrever.")
        return

    try:
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Cabeçalho do CSV
            header = ["ID", "CPU Usage", "Memory Usage", "Thread Count", "Error Count",
                      "Total Data Received", "Total Data Filtered", "Total Data Compressed",
                      "Total Data Aggregated", "Total Data After Heuristics"]
            writer.writerow(header)

            # Escrevendo as linhas de dados
            for metric in metrics_data:
                writer.writerow([
                    metric.get("id"),
                    metric.get("cpuUsage"),
                    metric.get("memoryUsage"),
                    metric.get("threadCount"),
                    metric.get("errorCount"),
                    metric.get("totalDataReceived"),
                    metric.get("totalDataFiltered"),
                    metric.get("totalDataCompressed"),
                    metric.get("totalDataAggregated"),
                    metric.get("totalDataAfterHeuristics"),
                ])

        print(f"CSV gerado com sucesso: {CSV_FILE_PATH}")
    except IOError as e:
        print(f"Erro ao escrever o arquivo CSV: {e}")


def main():
    metrics_data = fetch_metrics()
    if metrics_data:
        write_metrics_to_csv(metrics_data)
    else:
        print("Não foi possível obter métricas.")


if __name__ == "__main__":
    main()
