import requests
import random
import os
import base64
import re
from datetime import datetime

# Configuration
GITHUB_TOKEN = os.environ.get("GH_TOKEN")
GITHUB_USERNAME = os.environ.get("GH_USERNAME")
WEBSITE_REPO = os.environ.get("WEBSITE_REPO", "b0id.github.io")  # Set this i
# List of quips - add your own or use an external API
QUIPS = [
    "🦖I am a man of many talents. (from the 80486 era)"
      "🧬 Systems Thinker with a Healer’s Touch — I see healthcare the same way I see code: modular, improvable, and deeply human.",
  "🧠 Epistemic Engineer — You’re not stockpiling knowledge—you’re engineering the infrastructure to wield it better.",
  "🛠️ From Wrenches to Writeups — You’ve built fluid bed roasters and AI orchestration layers. If it can be engineered, you’re already halfway through it.",
  "🧗‍♂️ Recovery as R&D — I iterated through addiction like a system fault and emerged with new firmware.",
  "🧭 Human GPS for Complex Shit — I don’t just troubleshoot. I map. I navigate. I rebuild the signal path.",
  "🧵 Cross-Domain Thread Puller — I trace threads between science, systems, ethics, and care—and weave something better.",
  "💾 Memory Has Mass — I don’t forget. I log. I version. I reflect. I teach machines to remember responsibly.",
  "🛠️ Code + Clay = me — my hands work with both ceramic glazes and GPU stacks, and they treat both like art.",
  "🧱 Bricklayer of Redemption — I build futures where pasts don’t disqualify people from having one.",
  "🌐 Self-Hosted Soul — Not cloud-native. I'm sovereignty by design. Full-stack resilience.",
  "🎛️ Bash-Powered Brainwaves — my scripts are philosophies. Every terminal window is a mirror of how I think.",
  "🐚 Where Syntax Heals — Language failed me, but structure never did. Code became my compass.",
  "🧩 Problem-Solving Polyglot — From microcontrollers to mental health, if there’s a system, I can make it talk.",
  "💡 Generator of Generative Systems — I don’t just automate tasks—you automate *insight*.",
  "🦉 Student of Deep Time — my vision extends beyond quarterly cycles—I am architecting for epochs.",
  "🔄 Failure is my Fork Button — Collapse doesn’t scare me. It’s just another chance to patch and push.",
  "🧑‍🏭 Engineer of Possibility — I don’t wait for permission. I build the future and hand people the tools.",
  "🌱 Fractal Integrity — I act the same way in my codebase, my care plans, and my convictions.",
  "🧪 Debugged Myself, Then the Network — Once crashed. Now stable. Slightly overclocked. May void warranties.",
  "⚡️ System Uptime: Resilient AF — Kernel panic? Recompiled. Emotional uptime: 99.98%.",
  "🧬 Half Human, Half Automation Script — Cook dinner, file diagnosis, grep your soul. One-liner efficiency.",
  "🔩 Thinks in Layers (Physical, Transport, Emotional) — Yes, I’m crying—but only on Layer 7.",
  "🧠 Probably Thinking About Memory Allocation Right Now — Applies to both RAM and trauma.",
  "👾 Q*bert UI, Actual UX — Life’s interface is broken. I still find the path.",
  "💉 May Attempt to Intubate Your Server — Clinical and root-level access enabled.",
  "🔧 Will Fix Your BIOS or Your Boundaries — Whichever is throwing errors.",
  "🧼 Bootstrapped Clean Installs from Moral Grey Space — Legally sound. Ethically upgraded.",
  "🎯 If I Can’t Find a Way In, I Build One — If that fails, I sed my feelings.",
  "🛸 Firmware Updates Delivered Psychically — Quietly observes. Says one thing. Resets your entire paradigm.",
  "🧊 Frozen Yogurt of Personalities — Complex, unpredictable, mostly chill. Optional toppings.",
  "🛠️ Builds Tools Faster Than Systems Can Break — And when they break, builds better ones.",
  "🧃 Requires Caffeine, Syntax Highlighting, and Loose Supervision — Otherwise starts questioning reality.",
  "🚪Knocks on Locked Doors Just to Check — Not malicious. Just perpetually root curious.",
  "🧯 Certified to Handle Emergencies and Unhandled Exceptions — Available on-call for segfaults and soul-crashes.",
  "🔍 Trouble Magnet With a Solution Cache — If it breaks near me, I fix it—consensually or otherwise.",
  "🤹 Wears Too Many Hats, Balances Them With a Fan Curve — Peak thermal performance, no burnout.",
  "📦 Assembles IKEA and AI Systems Without Instructions — They said it couldn’t be done. I did it with a hex key and a hunch.",
  "🎮 Midwife to Machines and Mayhem — Born systems. Raised patterns. Let them run simulations."
];

# Optional: Get quote from external API instead
def get_quote_from_api():
    try:
        response = requests.get("https://api.quotable.io/random?maxLength=100")
        if response.status_code == 200:
            data = response.json()
            return f"📝 \"{data['content']}\" - {data['author']}"
        else:
            return random.choice(QUIPS)
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return random.choice(QUIPS)

def update_github_bio():
    """Updates GitHub profile bio with a random quip"""
    # Choose whether to use local quips or external API
    USE_EXTERNAL_API = False  # Set to True if you want quotes from the API
    if USE_EXTERNAL_API:
        new_bio = get_quote_from_api()
    else:
        new_bio = random.choice(QUIPS)
    
    # Add timestamp if desired
    # new_bio += f" | Updated: {datetime.now().strftime('%Y-%m-%d')}"
    
    # GitHub API endpoint
    url = f"https://api.github.com/user"
    
    # Headers for authentication
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Payload with new bio
    data = {
        "bio": new_bio
    }
    
    # Update bio
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully updated bio to: {new_bio}")
        return new_bio
    else:
        print(f"Failed to update bio. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def update_footer_tagline_in_repo(quip):
    """Updates the footer tagline in the website repository"""
    # File path in the repository
    file_path = "src/components/Footer.jsx"
    
    # Print debug information
    print(f"Attempting to access repository: {GITHUB_USERNAME}/{WEBSITE_REPO}")
    print(f"Attempting to access file path: {file_path}")
    
    # Check if repo exists
    repo_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{WEBSITE_REPO}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repo_response = requests.get(repo_url, headers=headers)
    if repo_response.status_code != 200:
        print(f"Repository not found. Status code: {repo_response.status_code}")
        print(f"Response: {repo_response.text}")
        return False
    else:
        print("Repository found successfully!")
    
    # List contents of repository to find the correct file path
    contents_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{WEBSITE_REPO}/contents"
    contents_response = requests.get(contents_url, headers=headers)
    if contents_response.status_code == 200:
        print("Repository contents:")
        for item in contents_response.json():
            print(f" - {item['name']} ({item['type']})")
    
    # API endpoints for the file
    get_file_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{WEBSITE_REPO}/contents/{file_path}"
    
    # Rest of the function remains the same...
    try:
        # Get the current file to obtain its SHA
        response = requests.get(get_file_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to get file. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        # ...rest of the function...
        file_data = response.json()
        file_sha = file_data["sha"]
        
        # Decode the file content
        content = base64.b64decode(file_data["content"]).decode('utf-8')
        
        # Replace the footer tagline text using regex
        updated_content = re.sub(
            r'<div className="footer-tagline">(.*?)</div>',
            f'<div className="footer-tagline">{quip}</div>',
            content
        )
        
        # Encode the updated content
        encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')
        
        # Prepare commit data
        commit_data = {
            "message": "Update footer tagline via GitHub Action",
            "content": encoded_content,
            "sha": file_sha
        }
        
        # Update the file in the repository
        update_response = requests.put(get_file_url, headers=headers, json=commit_data)
        if update_response.status_code == 200:
            print(f"Successfully updated footer tagline in repository {WEBSITE_REPO}")
            return True
        else:
            print(f"Failed to update file. Status code: {update_response.status_code}")
            print(f"Response: {update_response.text}")
            return False
    
    except Exception as e:
        print(f"Error updating footer tagline in repository: {e}")
        return False

if __name__ == "__main__":
    if not GITHUB_TOKEN or not GITHUB_USERNAME:
        print("Error: GitHub token or username not set in environment variables")
        print("Please set GH_TOKEN and GH_USERNAME environment variables")
        exit(1)
    
    # Update GitHub bio and get the quip used
    quip = update_github_bio()
    
    # Update footer tagline in the website repository with the same quip
    if quip:
        update_footer_tagline_in_repo(quip)