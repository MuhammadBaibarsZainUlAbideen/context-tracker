# Context Switching Tracker
Tracks how much time you lose switching between coding projects by analyzing git commits.

## Installation
```bash
git clone https://github.com/MuhammadBaibarsZainUlAbideen/context-tracker
cd context-tracker
pip install gitpython
```

## Setup
Edit `config.json`:
```json
{
  "scan_paths": ["C:\\Users\\YourName\\Desktop"],
  "author_email": "your@email.com",
  "switch_threshold_minutes": 30
}
```

## Usage
```bash
python scanner.py --today     # Today's switches
python scanner.py --week      # Last 7 days
python scanner.py --month     # Last 30 days
python scanner.py --days 90   # Custom range
```

## Example Output
```
CONTEXT SWITCHES: 4
15:43 - CS1083 → Java (gap: 74 min)
19:10 - Leet_Code → Mastering_Git (gap: 1220 min)
23:25 - Mastering_Git → Leet_Code (gap: 241 min)
18:25 - Leet_Code → Mastering_Git (gap: 1140 min)

STATS
Total switches: 4
Time lost: 1.3 hours (80 minutes)
```

## **Explanation**

### Understanding Context Switches

When you see a line like:
```
15:43 - CS1083 → Java (gap: 74 min)
```

**What it means:**
- **15:43** = Time of your first commit to the NEW repository (Java)
- **CS1083 → Java** = You switched FROM CS1083 TO Java  
- **gap: 74 min** = 74 minutes passed between your last CS1083 commit and your first Java commit

### Why This Matters
Research shows switching between projects costs ~20 minutes of focus time as you:
- Remember what you were working on
- Load the mental context
- Get back into flow state

**The tool tracks these switches to quantify your hidden productivity cost.**

## My Results
Over 90 days: 4 real switches, ~1.3 hours lost to context switching.

Building a dashboard version. Would you use this?
