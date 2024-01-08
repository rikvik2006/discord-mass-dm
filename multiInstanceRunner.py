import json
import time
import subprocess


def modify_config(guild_id, channel_id):
    # Modifica il file config.json
    config_path = "./data/config.json"
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
        config_data["cli_setup"]["scrape_user"]["guild_id"] = guild_id
        config_data["cli_setup"]["scrape_user"]["channel_id"] = channel_id

    with open(config_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)


def update_tokens(token):
    # Aggiungi il token all'array nel file tokens.json
    tokens_path = "./data/tokens.json"
    with open(tokens_path, "r") as tokens_file:
        tokens_data = json.load(tokens_file)
        token_data = [token]
        tokens_data = token_data

    with open(tokens_path, "w") as tokens_file:
        json.dump(tokens_data, tokens_file, indent=4)


def main():
    processes = []
    # Leggi il file instances_data.txt
    instances_file = "instances_data.txt"
    with open(f"./data/{instances_file}", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(";")[0].strip().split(",")
            token, guild_id, channel_id = data
            modify_config(guild_id, channel_id)
            update_tokens(token)
            # Avvia lo script main.py
            process = subprocess.Popen(["python", "main.py"])
            processes.append(process)
            print(f"Avviato processo con token {token}")
            time.sleep(1)

    print(
        f"⭐ Tutti i processi sono stati avviati per un totale di {len(processes)} processi ⭐"
    )


if __name__ == "__main__":
    main()
