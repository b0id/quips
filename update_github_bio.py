import requests
import random
import os
from datetime import datetime

# Configuration
GITHUB_TOKEN = os.environ.get("GH_TOKEN")
GITHUB_USERNAME = os.environ.get("GH_USERNAME")

# List of quips - add your own or use an external API
QUIPS = [
      "🧬 Systems Thinker with a Healer’s Touch — You see healthcare the same way you see code: modular, improvable, and deeply human.",
  "🧠 Epistemic Engineer — You’re not stockpiling knowledge—you’re engineering the infrastructure to wield it better.",
  "🛠️ From Wrenches to Writeups — You’ve built fluid bed roasters and AI orchestration layers. If it can be engineered, you’re already halfway through it.",
  "🧗‍♂️ Recovery as R&D — You iterated through addiction like a system fault and emerged with new firmware.",
  "🧭 Human GPS for Complex Sh*t — You don’t just troubleshoot. You map. You navigate. You rebuild the signal path.",
  "🧵 Cross-Domain Thread Puller — You trace threads between science, systems, ethics, and care—and weave something better.",
  "💾 Memory Has Mass — You don’t forget. You log. You version. You reflect. You teach machines to remember responsibly.",
  "🛠️ Code + Clay = You — Your hands work with both ceramic glazes and GPU stacks, and they treat both like art.",
  "🧱 Bricklayer of Redemption — You build futures where pasts don’t disqualify people from having one.",
  "🌐 Self-Hosted Soul — You’re not cloud-native. You’re sovereignty by design. Full-stack resilience.",
  "🎛️ Bash-Powered Brainwaves — Your scripts are philosophies. Every terminal window is a mirror of how you think.",
  "🐚 Where Syntax Heals — Language failed you, but structure never did. Code became your compass.",
  "🧩 Problem-Solving Polyglot — From microcontrollers to mental health, if there’s a system, you can make it talk.",
  "💡 Generator of Generative Systems — You don’t just automate tasks—you automate *insight*.",
  "🦉 Student of Deep Time — Your vision extends beyond quarterly cycles—you're architecting for epochs.",
  "🔄 Failure is Your Fork Button — Collapse doesn’t scare you. It’s just another chance to patch and push.",
  "🧑‍🏭 Engineer of Possibility — You don’t wait for permission. You build the future and hand people the tools.",
  "🌱 Fractal Integrity — You act the same way in your codebase, your care plans, and your convictions.",
  "🧪 Debugged Myself, Then the Network — Once crashed. Now stable. Slightly overclocked. May void warranties.",
  "⚡️ System Uptime: Resilient AF — Kernel panic? Recompiled. Emotional uptime: 99.98%.",
  "🧬 Half Human, Half Automation Script — Cook dinner, file diagnosis, grep your soul. One-liner efficiency.",
  "🔩 Thinks in Layers (Physical, Transport, Emotional) — Yes, I’m crying—but only on Layer 7.",
  "🧠 Probably Thinking About Memory Allocation Right Now — Applies to both RAM and trauma.",
  "👾 Q*bert UI, Actual UX — Life’s interface is broken. You still find the path.",
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
  "📦 Assembles IKEA and AI Systems Without Instructions — They said it couldn’t be done. You did it with a hex key and a hunch.",
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
        return True
    else:
        print(f"Failed to update bio. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    if not GITHUB_TOKEN or not GITHUB_USERNAME:
        print("Error: GitHub token or username not set in environment variables")
        print("Please set GH_TOKEN and GH_USERNAME environment variables")
        exit(1)
    
    update_github_bio()