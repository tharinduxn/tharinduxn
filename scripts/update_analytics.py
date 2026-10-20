#!/usr/bin/env python3
"""Render honest, self-contained profile cards using only Python's standard library.

Sources: GitHub's public REST API and the public contribution calendar.
No personal access token is required. GITHUB_TOKEN raises REST rate limits in CI.
No files are changed until all network requests and validation have succeeded.
"""

import datetime as dt
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "analytics"
USER = os.environ.get("PROFILE_USERNAME", "tharinduxn")
PALETTES = {
    "dark": dict(bg="#0d1117", fg="#f0f3f6", muted="#9da5ae", border="#30363d",
                 levels=["#161b22", "#3d444d", "#656c76", "#9da5ae", "#e6edf3"]),
    "light": dict(bg="#ffffff", fg="#1f2328", muted="#59636e", border="#d1d9e0",
                  levels=["#eff2f5", "#c8cdd3", "#929aa4", "#59636e", "#24292f"]),
}


def fetch(url):
    headers = {"User-Agent": "tharinduxn-profile-analytics", "Accept": "application/vnd.github+json"}
    if url.startswith("https://api.github.com/"):
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = "Bearer " + token
    else:
        headers["Accept"] = "text/html"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read().decode("utf-8")


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tips = {}
        self.tip_id = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-date" in attrs and "data-level" in attrs:
            self.cells[attrs["id"]] = (attrs["data-date"], int(attrs["data-level"]))
        if tag == "tool-tip" and attrs.get("for"):
            self.tip_id = attrs["for"]
            self.tips[self.tip_id] = ""

    def handle_data(self, data):
        if self.tip_id:
            self.tips[self.tip_id] += data

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.tip_id = None


def parse_calendar(markup, today):
    parser = CalendarParser()
    parser.feed(markup)
    result = {}
    for key, (date_string, level) in parser.cells.items():
        day = dt.date.fromisoformat(date_string)
        if day > today:
            continue
        tip = parser.tips.get(key, "").strip()
        match = re.match(r"(No|[\d,]+) contributions? on ", tip)
        if not match:
            raise ValueError("GitHub calendar markup changed: a daily contribution count is missing.")
        count = 0 if match[1] == "No" else int(match[1].replace(",", ""))
        if not 0 <= level <= 4 or (count == 0) != (level == 0):
            raise ValueError("GitHub calendar contains inconsistent levels or counts.")
        result[day] = {"date": day.isoformat(), "count": count, "level": level}
    start = today - dt.timedelta(days=364)
    required = [start + dt.timedelta(days=i) for i in range(365)]
    if any(day not in result for day in required):
        raise ValueError("GitHub did not return a complete, current 365-day calendar. Keeping existing cards.")
    return [result[day] for day in required]


def calculate_streaks(days):
    """Input must be one continuous, ascending window ending today (UTC)."""
    counts = [day["count"] for day in days]
    longest = run = 0
    for count in counts:
        run = run + 1 if count else 0
        longest = max(longest, run)
    # Today has not ended: an active streak through yesterday is still current.
    index = len(counts) - 1
    if index >= 0 and counts[index] == 0:
        index -= 1
    current = 0
    while index >= 0 and counts[index] > 0:
        current += 1
        index -= 1
    return current, longest


def text(x, y, value, size=13, fill="#f0f3f6", weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{html.escape(str(value))}</text>')


def svg(width, height, title, description, content, p):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>'
            f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="10" '
            f'fill="{p["bg"]}" stroke="{p["border"]}"/>'
            '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">'
            + "".join(content) + '</g></svg>\n')


def metric_card(title, subtitle, metrics, footer, p):
    content = [text(24, 32, title, 16, p["fg"], 600), text(24, 53, subtitle, 11, p["muted"])]
    for i, (value, label) in enumerate(metrics):
        x = 24 + (i % 2) * 182
        y = 100 + (i // 2) * 69
        content += [text(x, y, f"{value:,}", 30, p["fg"], 600), text(x, y+20, label, 12, p["muted"])]
    content += [text(24, 219, footer, 10, p["muted"])]
    description = "; ".join(f"{label}: {value}" for value, label in metrics)
    return svg(390, 238, title, description + ". " + footer, content, p)


def calendar_card(days, stamp, p, compact=False):
    width = 390 if compact else 790
    final = dt.date.fromisoformat(days[-1]["date"])
    sunday = final - dt.timedelta(days=(final.weekday()+1) % 7)
    if compact:
        start = sunday - dt.timedelta(weeks=12)
    else:
        first = dt.date.fromisoformat(days[0]["date"])
        start = first - dt.timedelta(days=(first.weekday()+1) % 7)
    columns = (sunday-start).days // 7 + 1
    step = 21 if compact else 13.2
    cell = step - 3
    x0 = 55 if compact else 53
    y0 = 87
    content = [text(24, 31, "Contribution calendar", 16, p["fg"], 600),
               text(24, 52, "Recent 13 weeks" if compact else "Past 365 days", 11, p["muted"])]
    month_seen = None
    for col in range(columns):
        day = start + dt.timedelta(weeks=col)
        if day.month != month_seen:
            # Keep the final partial month label inside the card.
            if col < columns-1:
                content.append(text(round(x0+col*step, 1), 75, day.strftime("%b"), 10, p["muted"]))
            month_seen = day.month
    for row, name in [(1,"M"),(3,"W"),(5,"F")]:
        content.append(text(25, round(y0 + row*step + cell-1, 1), name, 10, p["muted"]))
    visible = []
    for entry in days:
        day = dt.date.fromisoformat(entry["date"])
        if day < start:
            continue
        col, row = divmod((day-start).days, 7)
        x, y = x0+col*step, y0+row*step
        content.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" rx="2" '
                       f'fill="{p["levels"][entry["level"]]}"><title>{entry["date"]}: '
                       f'{entry["count"]} contributions</title></rect>')
        visible.append(entry)
    footer_y = round(y0+7*step+22)
    legend_x = width - 156
    content.append(text(legend_x-27, footer_y, "Less", 10, p["muted"]))
    for i, color in enumerate(p["levels"]):
        content.append(f'<rect x="{legend_x+i*14}" y="{footer_y-9}" width="10" height="10" rx="2" fill="{color}"/>')
    content += [text(legend_x+75, footer_y, "More", 10, p["muted"]),
                text(24, footer_y+23, f"{sum(d['count'] for d in visible):,} contributions in this view", 11, p["muted"]),
                text(24, footer_y+41, f"Updated {stamp} UTC", 10, p["muted"])]
    return svg(width, footer_y+57, "Contribution calendar", "Daily GitHub activity. " + "; ".join(
        f"{d['date']}: {d['count']}" for d in visible), content, p)


def activity_card(days, stamp, p, compact=False):
    recent = days[-30:]
    width = 390 if compact else 790
    total = sum(d["count"] for d in recent)
    active = sum(d["count"] > 0 for d in recent)
    content = [text(24,31,"Recent activity",16,p["fg"],600),
               text(24,53,f"{total:,} contributions / {active} active days / last 30 days",11,p["muted"])]
    chart_x, chart_y, chart_h = 42, 82, 90
    chart_w = width - 66
    maximum = max(1,max(d["count"] for d in recent))
    for value in [0, maximum]:
        y = chart_y+chart_h-value/maximum*chart_h
        content += [f'<path d="M {chart_x} {y} H {width-24}" stroke="{p["border"]}"/>',
                    text(chart_x-8,y+3,value,9,p["muted"],anchor="end")]
    slot = chart_w/30
    for i, day in enumerate(recent):
        if day["count"] == 0:
            continue
        h = day["count"] / maximum * chart_h
        content.append(f'<rect x="{chart_x+i*slot+1:.2f}" y="{chart_y+chart_h-h:.2f}" '
                       f'width="{max(2,slot-3):.2f}" height="{h:.2f}" rx="1.5" fill="{p["fg"]}">'
                       f'<title>{day["date"]}: {day["count"]} contributions</title></rect>')
    date_label = lambda entry: dt.date.fromisoformat(entry["date"]).strftime("%d %b")
    content += [text(chart_x,192,date_label(recent[0]),10,p["muted"]),
                text(width-24,192,date_label(recent[-1]),10,p["muted"],anchor="end"),
                text(24,220,f"Daily contributions / Updated {stamp} UTC",10,p["muted"])]
    return svg(width,238,"Last 30 days of GitHub activity","; ".join(
        f"{d['date']}: {d['count']} contributions" for d in recent),content,p)


def collect(today):
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", USER):
        raise ValueError("Invalid GitHub username")
    user = json.loads(fetch(f"https://api.github.com/users/{USER}"))
    repos = []
    page = 1
    while True:
        batch = json.loads(fetch(f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}"))
        if not isinstance(batch, list):
            raise ValueError("GitHub repositories response was not a list")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    days = parse_calendar(fetch(f"https://github.com/users/{USER}/contributions"), today)
    current, longest = calculate_streaks(days)
    return dict(username=USER, as_of=today.isoformat(), public_repositories=user["public_repos"],
                stars=sum(r["stargazers_count"] for r in repos if not r["fork"]),
                followers=user["followers"], contributions=sum(d["count"] for d in days),
                current_streak=current, longest_streak_365_days=longest,
                active_days_365=sum(d["count"] > 0 for d in days),
                active_days_30=sum(d["count"] > 0 for d in days[-30:]), days=days,
                sources=[f"https://api.github.com/users/{USER}",
                         f"https://api.github.com/users/{USER}/repos",
                         f"https://github.com/users/{USER}/contributions"])


def render(data):
    stamp = data["as_of"]
    files = {}
    for theme,p in PALETTES.items():
        files[f"stats-{theme}.svg"] = metric_card("GitHub overview", "@"+data["username"], [
            (data["contributions"],"Contributions / 365 days"),
            (data["public_repositories"],"Public repositories"),
            (data["stars"],"Stars / original repos"),
            (data["followers"],"Followers"),
        ], f"Updated {stamp} UTC",p)
        files[f"streak-{theme}.svg"] = metric_card("Contribution streaks", "Consecutive active days / UTC", [
            (data["current_streak"],"Current streak"),
            (data["longest_streak_365_days"],"Longest / 365 days"),
            (data["active_days_365"],"Active days / 365 days"),
            (data["active_days_30"],"Active days / 30 days"),
        ], "Today may continue a streak through yesterday.",p)
        for compact in [False,True]:
            suffix = "-mobile" if compact else ""
            files[f"calendar{suffix}-{theme}.svg"] = calendar_card(data["days"],stamp,p,compact)
            files[f"activity{suffix}-{theme}.svg"] = activity_card(data["days"],stamp,p,compact)
    files["data.json"] = json.dumps(data,indent=2)+"\n"
    # Build the complete output first; a fetch/parse/render failure leaves the last good snapshot intact.
    OUT.mkdir(parents=True,exist_ok=True)
    for name,content in files.items():
        target = OUT / name
        temporary = target.with_suffix(target.suffix+".tmp")
        temporary.write_text(content,encoding="utf-8")
        temporary.replace(target)
    print(f"Rendered {len(files)-1} cards for {data['username']} as of {stamp}.")


if __name__ == "__main__":
    try:
        render(collect(dt.datetime.now(dt.timezone.utc).date()))
    except (urllib.error.URLError,ValueError,KeyError,TypeError) as exc:
        print(f"Analytics refresh failed; existing cards were retained. {exc}",file=sys.stderr)
        sys.exit(1)
