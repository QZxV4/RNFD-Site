import requests
import os

def download_github_file(token, repo_owner, repo_name, file_path, branch="main", output_filename=None):
    """
    Downloads a file from a GitHub repository using a Personal Access Token.

    Parameters:
        token (str): GitHub Personal Access Token
        repo_owner (str): GitHub username or organization
        repo_name (str): Repository name
        file_path (str): Path to the file in the repo
        branch (str): Branch name (default is 'main')
        output_filename (str): Local filename to save as (defaults to file_path basename)
    """
    if output_filename is None:
        output_filename = os.path.basename(file_path)

    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ File downloaded successfully: {output_filename}")
    else:
        print(f"❌ Failed to download file. Status code: {response.status_code}")
        print(f"Message: {response.text}")

# --- Example usage ---
if __name__ == "__main__":
    GITHUB_TOKEN = "ghp_your_personal_access_token_here"  # Replace this
    REPO_OWNER = "qzxv4"
    REPO_NAME = "Reddit-Notifier-For-Discord"
    FILE_PATH = "python/main.py"
    BRANCH = "main"  # Change if needed

    download_github_file(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, FILE_PATH, BRANCH)
