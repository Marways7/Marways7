import json
import math
import os
import urllib.request
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.error import URLError, HTTPError


WIDTH = 800
HEIGHT = 280
REQUEST_TIMEOUT = 20
REPO_PAGE_SIZE = 100
CONTRIBUTIONS_LOOKBACK_DAYS = 365
HEXAGON_INNER_RADIUS = 75
HEXAGON_OUTER_RADIUS = 85
GITHUB_API_VERSION = "2022-11-28"
GITHUB_REST_API_ROOT = "https://api.github.com"
GITHUB_GRAPHQL_API_URL = f"{GITHUB_REST_API_ROOT}/graphql"
GITHUB_USER = os.environ.get("GITHUB_USER", "Marways7")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
METRICS_OUTPUT_PATH = Path("assets/sota-metrics.svg")
REPOS_LIST_QUERY = f"per_page={REPO_PAGE_SIZE}&type=owner"
GITHUB_USER_AGENT = "Marways7-profile-generator"
THOUSAND = 1_000
MILLION = 1_000_000

DEFAULT_METRICS = {
    "repo_count": "7",
    "star_count": "10",
    "contributions_year": "110",
    "created_year": "2023",
}

CONTRIBUTIONS_QUERY = """
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


HEXAGON_UNIT_VECTORS = [
    (math.cos(math.radians(60 * i - 30)), math.sin(math.radians(60 * i - 30)))
    for i in range(6)
]


GITHUB_BASE_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": GITHUB_API_VERSION,
    "User-Agent": GITHUB_USER_AGENT,
}


def build_headers():
    headers = GITHUB_BASE_HEADERS.copy()
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def read_json_response(request):
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def github_get(url):
    request = urllib.request.Request(url, headers=build_headers())
    return read_json_response(request)


def github_graphql(query, variables):
    if not GITHUB_TOKEN:
        raise URLError("GITHUB_TOKEN is required for GraphQL contribution queries")

    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        GITHUB_GRAPHQL_API_URL,
        data=payload,
        headers={
            **build_headers(),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    data = read_json_response(request)

    if data.get("errors"):
        raise URLError(f"GraphQL errors: {data['errors']}")

    return data["data"]


def format_compact(value):
    if value >= MILLION:
        return f"{value / MILLION:.1f}M".rstrip("0").rstrip(".")
    if value >= THOUSAND:
        return f"{value / THOUSAND:.1f}k".rstrip("0").rstrip(".")
    return str(value)


def extract_created_year(user):
    created_at = user.get("created_at")
    if isinstance(created_at, str) and len(created_at) >= 4:
        return created_at[:4]
    return DEFAULT_METRICS["created_year"]


def fetch_live_metrics():
    user_api_root = f"{GITHUB_REST_API_ROOT}/users/{GITHUB_USER}"
    user = github_get(user_api_root)

    public_repo_count = int(user.get("public_repos", 0) or 0)
    repo_pages = (public_repo_count + REPO_PAGE_SIZE - 1) // REPO_PAGE_SIZE
    repos_api_prefix = f"{user_api_root}/repos?{REPOS_LIST_QUERY}"
    total_stars = 0
    total_repos = 0

    for repo_page in range(1, repo_pages + 1):
        repos = github_get(f"{repos_api_prefix}&page={repo_page}")
        total_repos += len(repos)
        total_stars += sum(repo.get("stargazers_count", 0) for repo in repos)

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=CONTRIBUTIONS_LOOKBACK_DAYS)
    contributions_data = github_graphql(
        CONTRIBUTIONS_QUERY,
        {
            "login": GITHUB_USER,
            "from": start_date.isoformat(),
            "to": end_date.isoformat(),
        },
    )
    user_contributions = contributions_data.get("user") or {}
    contribution_collection = user_contributions.get("contributionsCollection") or {}
    contribution_calendar = contribution_collection.get("contributionCalendar") or {}
    total_contributions = int(contribution_calendar.get("totalContributions", 0) or 0)

    return {
        "repo_count": format_compact(total_repos or public_repo_count),
        "star_count": format_compact(total_stars),
        "contributions_year": format_compact(total_contributions),
        "created_year": extract_created_year(user),
    }


def load_metrics():
    try:
        metrics = fetch_live_metrics()
        print(f"Fetched live metrics for {GITHUB_USER}: {metrics}")
        return metrics
    except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"Failed to fetch live metrics for {GITHUB_USER}: {exc}")
        print("Using fallback metrics so SVG generation can still complete.")
        return DEFAULT_METRICS.copy()


def draw_hexagon(cx, cy, radius):
    return " ".join(
        f"{cx + radius * unit_x},{cy + radius * unit_y}"
        for unit_x, unit_y in HEXAGON_UNIT_VECTORS
    )


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
        hex_str = draw_hexagon(cx, cy, HEXAGON_INNER_RADIUS)
        outer_hex = draw_hexagon(cx, cy, HEXAGON_OUTER_RADIUS)
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
    METRICS_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_OUTPUT_PATH.write_text(build_svg(metrics), encoding="utf-8")
    print(f"SOTA live metrics hologram generated at {METRICS_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
