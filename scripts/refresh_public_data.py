"""Refresh public repository metadata only; no private repositories or personal data."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Marways-profile"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    result = []
    for page in range(1, 101):
        req = Request(f"https://api.github.com/users/Marways7/repos?type=owner&per_page=100&page={page}", headers=headers)
        with urlopen(req, timeout=30) as response:
            repos = json.load(response)
        if not isinstance(repos, list):
            raise ValueError("Expected a repository list")
        for repo in repos:
            if repo.get("private", True):
                continue
            result.append({k: repo[k] for k in ("name", "html_url", "language", "stargazers_count", "forks_count")})
        if len(repos) < 100:
            break
    else:
        raise RuntimeError("Pagination exceeded safety limit")
    if not result:
        raise ValueError("Empty response; preserving the last valid snapshot")
    data = {"updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": "https://api.github.com/users/Marways7/repos", "repositories": sorted(result, key=lambda r:r["name"])}
    target = ROOT / "data/public-profile.json"
    target.parent.mkdir(exist_ok=True)
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    print(f"Updated {len(result)} public repositories")


if __name__ == "__main__":
    main()
