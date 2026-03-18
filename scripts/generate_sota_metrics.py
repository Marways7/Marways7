import json
import math
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from urllib.error import URLError, HTTPError


WIDTH = 800
HEIGHT = 280
GITHUB_USER = os.environ.get("GITHUB_USER", "Marways7")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

DEFAULT_METRICS = {
    "repo_count": "18",
    "star_count": "51",
    "contributions_year": "850+",
    "created_year": "2020",
}


def build_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Marways7-profile-generator",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def github_get(url):
    request = urllib.request.Request(url, headers=build_headers())
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def github_graphql(query, variables):
    if not GITHUB_TOKEN:
        raise URLError("GITHUB_TOKEN is required for GraphQL contribution queries")

    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            **build_headers(),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    if data.get("errors"):
        raise URLError(f"GraphQL errors: {data['errors']}")

    return data["data"]


def format_compact(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M".rstrip("0").rstrip(".")
    if value >= 1_000:
        return f"{value / 1_000:.1f}k".rstrip("0").rstrip(".")
    return str(value)


def fetch_live_metrics():
    user = github_get(f"https://api.github.com/users/{GITHUB_USER}")

    repo_page = 1
    total_stars = 0
    total_repos = 0

    while True:
        repos = github_get(
            f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&page={repo_page}&type=owner"
        )
        if not repos:
            break

        total_repos += len(repos)
        total_stars += sum(repo.get("stargazers_count", 0) for repo in repos)
        repo_page += 1

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=365)
    contributions_query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """
    contributions_data = github_graphql(
        contributions_query,
        {
            "login": GITHUB_USER,
            "from": start_date.isoformat(),
            "to": end_date.isoformat(),
        },
    )
    total_contributions = (
        contributions_data["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    )

    return {
        "repo_count": format_compact(total_repos or user.get("public_repos", 0)),
        "star_count": format_compact(total_stars),
        "contributions_year": format_compact(total_contributions),
        "created_year": str(user.get("created_at", "2020"))[:4],
    }


def load_metrics():
    try:
        metrics = fetch_live_metrics()
        print(f"Fetched live metrics for {GITHUB_USER}: {metrics}")
        return metrics
    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Failed to fetch live metrics for {GITHUB_USER}: {exc}")
        print("Using fallback metrics so SVG generation can still complete.")
        return DEFAULT_METRICS.copy()


def draw_hexagon(cx, cy, radius):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        points.append(f"{cx + radius * math.cos(angle_rad)},{cy + radius * math.sin(angle_rad)}")
    return " ".join(points)


METRIC_LAYOUT = [
    {"key": "repo_count", "label": "TOTAL REPOSITORIES", "cx": 140, "cy": 140, "delay": 0},
    {"key": "star_count", "label": "STARS EARNED", "cx": 310, "cy": 140, "delay": 0.4},
    {"key": "contributions_year", "label": "CONTRIBUTIONS/YR", "cx": 480, "cy": 140, "delay": 0.8},
    {"key": "created_year", "label": "VIBE SINCE", "cx": 650, "cy": 140, "delay": 1.2},
]


def build_svg(metrics):
    svg_parts = [
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="auto">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&amp;family=Fira+Code:wght@600&amp;display=swap');
      
      .bg {{ fill: #0D1117; }}
      
      .hex-frame {{
        fill: rgba(139, 92, 246, 0.05);
        stroke: #A78BFA;
        stroke-width: 2;
        filter: drop-shadow(0 0 10px rgba(167, 139, 250, 0.4));
      }}
      .hex-frame:hover {{
        fill: rgba(6, 182, 212, 0.1);
        stroke: #06B6D4;
        filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.8));
      }}
      
      .value {{
        font-family: 'Orbitron', sans-serif;
        font-size: 34px;
        font-weight: 900;
        fill: #67E8F9;
        text-anchor: middle;
      }}
      .label {{
        font-family: 'Fira Code', monospace;
        font-size: 14px;
        font-weight: 600;
        fill: #8B949E;
        text-anchor: middle;
      }}
      @keyframes float-hex {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-6px); }}
      }}
      
      @keyframes pulse-ring {{
        0% {{ stroke-dasharray: 0 100; opacity: 0.8; }}
        100% {{ stroke-dasharray: 100 0; opacity: 0; }}
      }}
    </style>
  </defs>

  <rect width="100%" height="100%" class="bg" rx="15" />
"""
    ]

    for panel in METRIC_LAYOUT:
        cx, cy, delay = panel["cx"], panel["cy"], panel["delay"]
        hex_str = draw_hexagon(cx, cy, 75)
        outer_hex = draw_hexagon(cx, cy, 85)
        value = metrics[panel["key"]]
        label = panel["label"]

        svg_parts.append(
            f"""
  <g style="animation: float-hex 4s infinite {delay}s ease-in-out; transform-origin: {cx}px {cy}px;">
    <polygon points="{outer_hex}" fill="none" class="hex-frame" style="animation: pulse-ring 3s infinite {delay}s linear;" />
    <polygon points="{hex_str}" class="hex-frame" />
    <text x="{cx}" y="{cy + 10}" class="value">{value}</text>
    <text x="{cx}" y="{cy + 40}" class="label">{label}</text>
  </g>
"""
        )

    svg_parts.append("</svg>\n")
    return "".join(svg_parts)


def main():
    metrics = load_metrics()
    os.makedirs("assets", exist_ok=True)
    with open("assets/sota-metrics.svg", "w", encoding="utf-8") as output:
        output.write(build_svg(metrics))
    print("SOTA live metrics hologram generated at assets/sota-metrics.svg")


if __name__ == "__main__":
    main()
