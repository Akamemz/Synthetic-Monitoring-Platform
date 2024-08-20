#%%
import yaml
import json
import time
import pingparsing
from prometheus_client import start_http_server, Gauge


# Function to load a YAML file and return save it in an object
def yaml_loader(file_path):
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)  # we use safe_load for secure way of opening YAML files
            print("File loaded successfully")
            return data
    except FileNotFoundError:
        print("No such file or directory")

    return None

# Testing YAML loader with the custom file
# yaml_loader("z Sample Project/OpenAVE_2/output.yaml")


# ==============================================
#   Main Monitoring function with Prometheus
# ==============================================


# Define Prometheus metrics
PING_LATENCY = Gauge('ping_latency_seconds', 'Ping latency in seconds', ['server'])
PING_PACKET_LOSS = Gauge('ping_packet_loss', 'Ping packet loss in percentage', ['server'])


# Function to ping a server and return the results
def ping_server(server):
    p = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = server
    transmitter.count = 5  # Number of pings to send

    result = transmitter.ping()
    return p.parse(result).as_dict()


# Monitoring function that loops through the servers
def monitor_servers(servers, interval):
    while True:
        for server in servers:
            print(f"\nPinging {server}...")
            results = ping_server(server)
            print(json.dumps(results, indent=20))

            # Update Prometheus metrics
            latency = results.get('rtt_avg', None)
            packet_loss = results.get('packet_loss_rate', None)

            if latency is not None:
                PING_LATENCY.labels(server=server).set(latency)
            if packet_loss is not None:
                PING_PACKET_LOSS.labels(server=server).set(packet_loss)

        print(f"Waiting for {interval} seconds before the next round of pings...")
        time.sleep(interval)


# Main function to load the configuration and start monitoring
def main():
    config = yaml_loader(input("Input path for the YAML file: "))  # Provide a path for the YAML config file
    if config:
        servers = config.get('servers', [])
        interval = config.get('interval', 10)  # Default to 10 seconds if not specified

        # Start Prometheus metrics server
        start_http_server(8000)
        monitor_servers(servers, interval)


if __name__ == "__main__":
    main()



#%%
# # ==================================
# # Convert from .yaml to .json format
# # ==================================
# def yaml_to_json(input_file_path, output_file_path):
#     try:
#         with open(input_file_path, 'r') as file:
#             configurations = yaml.safe_load(file)
#
#         # Write the configuration to a JSON file
#         json_string = json.dumps(configurations, indent=2)
#
#         # Write the JSON to a file
#         with open(output_file_path, 'w') as json_file:
#             json_file.write(json_string)
#
#         print("File loaded successfully")
#         return json_string
#
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#     except yaml.YAMLError as e:
#         print(f"YAML Error: {e}")
#     except json.JSONDecodeError as e:
#         print(f"JSON Error: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#
#     return None


# # ==================================
# # Convert from .json to .yaml format
# # ==================================
# def json_to_yaml(file_path):
#     try:
#         # Read the JSON file
#         with open(file_path, 'r') as file:
#             configurations = json.load(file)
#
#         # Convert JSON to YAML and write to file
#         with open('config.yaml', 'w') as yaml_file:
#             yaml.dump(configurations, yaml_file, default_flow_style=False)
#
#         # Read the YAML file and return its content
#         with open('config.yaml', 'r') as yaml_file:
#             yaml_content = yaml_file.read()
#
#         print("File converted successfully")
#         return yaml_content
#
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#     except json.JSONDecodeError as e:
#         print(f"JSON Error: {e}")
#     except yaml.YAMLError as e:
#         print(f"YAML Error: {e}")
#     except IOError as e:
#         print(f"IO Error: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#
#     return None


#
# def display_results(results):
#     print("\nPing Results:")
#     print(json.dumps(results, indent=4))
#
#
# def main():
#     server = input("Enter the server or IP address to ping: ")
#     results = ping_server(server)
#     display_results(results)

# def monitor_servers(servers, interval):
#     while True:
#         for server in servers:
#             print(f"\nPinging {server}...")
#             results = ping_server(server)
#             print(json.dumps(results, indent=5))
#         print(f"Waiting for {interval} seconds before the next round of pings...")
#         time.sleep(interval)
#
#
# def main():
#     config = yaml_loader(input("Input path for the YAML file"))  # Provide a path for the YAML config file
#     if config:
#         servers = config.get('servers', [])
#         interval = config.get('interval', 10)  # Default to 10 seconds if not specified
#         monitor_servers(servers, interval)
#
#
# if __name__ == "__main__":
#     main()