import requests
from colorama import init, Fore, Style

init(autoreset=True)

def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        return [repo['name'] for repo in repos]
    else:
        print(f"{Fore.CYAN}Erreur lors de la récupération des dépôts de {username}{Style.RESET_ALL}")
        return None

def get_commits(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        commits = response.json()
        return commits
    else:
        print(f"{Fore.CYAN}Erreur lors de la récupération des commits pour le repo {repo_name}{Style.RESET_ALL}")
        return None

def get_commit_patch(username, repo_name, commit_sha):
    url = f"https://github.com/{username}/{repo_name}/commit/{commit_sha}.patch"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"{Fore.CYAN}Erreur lors de la récupération du patch pour le commit {commit_sha}{Style.RESET_ALL}")
        return None

def print_welcome_message():
    print(f"{Fore.CYAN}"
          """
                                          /^§
                       L L               /   \               L L
                    __/|/|_             /  .  \             _|\|\__
                   /_| [_[_\           /     .-\           /_]_] |_\§
                  /__\  __`-\_____    /    .    \    _____/-`__  /__\§
                 /___] /=@>  _   {>  /-.         \  <}   _  <@=\ [___\§
                /____/     /` `--/  /      .      \  \--` `\     \____\§
               /____/  \____/`-._> /               \ <_.-`\____/  \____\§
              /____/    /__/      /-._     .   _.-  \      \__\    \____\§
             /____/    /__/      /         .         \      \__\    \____\§
            |____/_  _/__/      /          .          \      \__\_  _\____|
             \__/_ ``_|_/      /      -._  .        _.-\      \_|_`` _\___/
               /__`-`__\      <_         `-;        NDT_>      /__`-`__\§
                  `-`           `-._       ;       _.-`           `-`
                                    `-._   ;   _.-`
                                        `-._.-`
          """)

def main():
    print_welcome_message()
    username = input(f"{Fore.CYAN}Entrez le nom d'utilisateur GitHub : {Style.RESET_ALL}")
    
    repos = get_user_repos(username)
    if repos:
        print(f"\n{Fore.CYAN}L'utilisateur {username} a les dépôts suivants :{Style.RESET_ALL}")
        for i, repo in enumerate(repos, 1):
            print(f"{i}. {Fore.CYAN}{repo}{Style.RESET_ALL}")

        repo_index = int(input(f"{Fore.CYAN}Choisissez le numéro du dépôt à consulter : {Style.RESET_ALL}")) - 1
        chosen_repo = repos[repo_index]

        commits = get_commits(username, chosen_repo)
        if commits:
            print(f"\n{Fore.CYAN}Les derniers commits pour le dépôt {chosen_repo} :{Style.RESET_ALL}")
            for i, commit in enumerate(commits, 1):
                sha = commit['sha']
                message = commit['commit']['message']
                print(f"{i}. {Fore.GREEN}{sha[:7]} - {message}{Style.RESET_ALL}")

            commit_index = int(input(f"{Fore.CYAN}Choisissez le numéro du commit pour voir le patch : {Style.RESET_ALL}")) - 1
            chosen_commit = commits[commit_index]['sha']

            patch = get_commit_patch(username, chosen_repo, chosen_commit)
            if patch:
                print(f"\n{Fore.CYAN}Voici le contenu du patch :{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{patch}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()