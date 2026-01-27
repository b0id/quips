import requests
import random
import os
import base64
import re
import sys

# Configuration
GITHUB_TOKEN = os.environ.get("GH_TOKEN")
GITHUB_USERNAME = os.environ.get("GH_USERNAME")
WEBSITE_REPO = os.environ.get("WEBSITE_REPO", "b0id.github.io")

# List of quips
QUIPS = [

    "🌹Roses are red, violets are blue, intelligence is learned, can you learn too?",
    "😎Catch you in the next merge conflict. ",
    "🦖 I am a man of many talents. (from the 80486 era)",
    "🧬 Systems Thinker with a Healer's Touch — I see healthcare the same way I see code: modular, improvable, and deeply human.",
    "🧠 Epistemic Engineer — You're not stockpiling knowledge—you're engineering the infrastructure to wield it better.",
    "🛠️ From Wrenches to Writeups — I've built fluid bed roasters and AI orchestration layers. If it can be engineered, I am already halfway through it.",
    "🧗‍♂️ Recovery as R&D — I iterated through addiction like a system fault and emerged with new firmware.",
    "🧭 Human GPS for Complex Shit — I don't just troubleshoot. I map. I navigate. I rebuild the signal path.",
    "🧵 Cross-Domain Thread Puller — I trace threads between science, systems, ethics, and care—and weave something better.",
    "💾 Memory Has Mass — I don't forget. I log. I version. I reflect. I teach machines to remember responsibly.",
    "🛠️ Code + Clay = me — my hands work with both ceramic glazes and GPU stacks, and they treat both like art.",
    "🧱 Bricklayer of Redemption — I build futures where pasts don't disqualify people from having one.",
    "🌐 Self-Hosted Soul — Not cloud-native. I'm sovereignty by design. Full-stack resilience.",
    "🎛️ Bash-Powered Brainwaves — my scripts are philosophies. Every terminal window is a mirror of how I think.",
    "🐚 Where Syntax Heals — Language failed me, but structure never did. Code became my compass.",
    "🧩 Problem-Solving Polyglot — From microcontrollers to mental health, if there's a system, I can make it talk.",
    "💡 Generator of Generative Systems — I don't just automate tasks—I automate insight.",
    "🦉 Student of Deep Time — my vision extends beyond quarterly cycles—I am architecting for epochs.",
    "🔄 Failure is my Fork Button — Collapse doesn't scare me. It's just another chance to patch and push.",
    "🧑‍🏭 Engineer of Possibility — I don't wait for permission. I build the future and hand people the tools.",
    "🌱 Fractal Integrity — I act the same way in my codebase, my care plans, and my convictions."
]

def get_random_quip():
    return random.choice(QUIPS)

def update_github_bio(quip):
    url = "https://api.github.com/user"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.patch(url, headers=headers, json={"bio": quip})
    if response.status_code == 200:
        print(f"✅ GitHub bio updated: {quip}")
        return True
    else:
        print(f"❌ GitHub bio update failed ({response.status_code}): {response.text}")
        return False

def verify_and_get_file(headers, repo, path_parts):
    base_url = f"https://api.github.com/repos/{repo}/contents"
    current_path = ""
    for i, part in enumerate(path_parts):
        current_url = f"{base_url}/{current_path}" if current_path else base_url
        print(f"📁 Checking: {current_url}")
        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed at {current_url} ({response.status_code})")
            return None
        contents = response.json()
        match = next((item for item in contents if item["name"] == part), None)
        if not match:
            print(f"❌ '{part}' not found.")
            return None
        if i == len(path_parts) - 1:
            if match["type"] != "file":
                print(f"❌ '{part}' is not a file.")
                return None
            print(f"✅ Found file: {match['path']}")
            return {"sha": match["sha"], "path": match["path"].lstrip("/")}
        else:
            if match["type"] != "dir":
                print(f"❌ '{part}' is not a directory.")
                return None
            current_path = f"{current_path}/{part}" if current_path else part
    return None

def update_footer_tagline(quip):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo = f"{GITHUB_USERNAME}/{WEBSITE_REPO}"
    path_parts = ["src", "components", "Footer.jsx"]
    file_info = verify_and_get_file(headers, repo, path_parts)

    if not file_info:
        print("❌ Could not locate Footer.jsx")
        return False

    file_url = f"https://api.github.com/repos/{repo}/contents/{file_info['path']}"
    print(f"📄 Preparing to patch: {file_url}")
    get_response = requests.get(file_url, headers=headers)
    if get_response.status_code != 200:
        print(f"❌ File fetch failed ({get_response.status_code})")
        print(get_response.text)
        return False

    file_data = get_response.json()
    decoded = base64.b64decode(file_data["content"]).decode("utf-8")

    updated = re.sub(
        r'<div className="footer-tagline">(.*?)</div>',
        f'<div className="footer-tagline">{quip}</div>',
        decoded
    )

    if updated == decoded:
        print("⚠️ No changes made. Tagline div unchanged or missing.")
        return False

    encoded = base64.b64encode(updated.encode("utf-8")).decode("utf-8")
    commit_data = {
        "message": f"Update footer tagline: {quip}",
        "content": encoded,
        "sha": file_info["sha"]
    }

    put_response = requests.put(file_url, headers=headers, json=commit_data)
    if put_response.status_code == 200:
        print(f"✅ Footer.jsx updated with new tagline.")
        return True
    else:
        print(f"❌ Failed to update Footer.jsx ({put_response.status_code})")
        print(put_response.text)
        return False

if __name__ == "__main__":
    if not GITHUB_TOKEN or not GITHUB_USERNAME:
        print("❌ GH_TOKEN or GH_USERNAME missing.")
        sys.exit(1)

    quip = get_random_quip()
    bio_success = update_github_bio(quip)
    footer_success = update_footer_tagline(quip)

    # Exit with error if either operation failed
    if not bio_success or not footer_success:
        print("\n❌ One or more updates failed. Check logs above.")
        sys.exit(1)
    else:
        print("\n✅ All updates completed successfully!")
        sys.exit(0)
