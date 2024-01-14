import json
import time
import subprocess
import requests
import os


def modify_config(guild_id, channel_id, blacklisted_roles: list):
    # Modify the config.json file
    config_path = "./data/config.json"
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
        config_data["blacklisted_roles"].clear()
        config_data["cli_setup"]["scrape_user"]["guild_id"] = guild_id
        config_data["cli_setup"]["scrape_user"]["channel_id"] = channel_id
        config_data["blacklisted_roles"].extend(blacklisted_roles)

    with open(config_path, "w") as config_file:
        json.dump(config_data, config_file, indent=4)


def update_tokens(token):
    # Add the token to the tokens.json file
    tokens_path = "./data/tokens.json"
    with open(tokens_path, "r") as tokens_file:
        tokens_data = json.load(tokens_file)
        token_data = [token]
        tokens_data = token_data

    with open(tokens_path, "w") as tokens_file:
        json.dump(tokens_data, tokens_file, indent=4)


def main():
    processes = []
    runner_config = "runner_config.json"
    instances_file = "instances_data.txt"
    with open(f"./data/{runner_config}", "r") as file:
        runner_data = json.load(file)
        use_tmux = runner_data["use_tmux"]
        logs_dir = runner_data["logs_dir"]

    # Get the tokens from instances_data.txt
    with open(f"./data/{instances_file}", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(";")[0].strip().split(",")
            token, guild_id, channel_id, *blacklisted_roles = data
            modify_config(guild_id, channel_id, blacklisted_roles)
            update_tokens(token)

            # Get the discord username
            response = requests.get(
                "https://discord.com/api/users/@me",
                headers={"authorization": token},
            )
            discord_username = response.json()["username"]

            # Start main.py
            if use_tmux:
                if logs_dir[-1] == "/" or logs_dir[-1] == "\\":
                    formatted_logs_dir = logs_dir[:-1] + "/"
                else:
                    formatted_logs_dir = logs_dir + "/"
                os.system(f"mkdir -p {formatted_logs_dir}")

                command = [
                    "tmux",
                    "new",
                    "-d",
                    "-s",
                    f"mass-dm-{discord_username}",
                    f"exec python3 ./main.py 2>&1 | tee -a {formatted_logs_dir}{discord_username}.log",
                ]

                try:
                    process = subprocess.Popen(command)
                    process.communicate()
                    processes.append(process)
                    print(
                        f"☕ [TMUX] Process started: Username: {discord_username}, Token: {token}"
                    )
                    time.sleep(1)
                except subprocess.CalledProcessError as e:
                    print(f"Errore nell'esecuzione del comando: {e}")
                except Exception as e:
                    print(f"Errore sconosciuto: {e}")
            else:
                process = subprocess.Popen(["python", "main.py"])
                processes.append(process)
                print(
                    f"☕ [CONSOLE] Process started: Username: {discord_username}, Token: {token}"
                )
                time.sleep(1)

    print(f"⭐ All processes were started for a total of {len(processes)} processes ⭐")


if __name__ == "__main__":
    main()
