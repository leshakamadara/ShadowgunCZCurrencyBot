# Shadow Gun Deadzone - Currency Exchange Bot

![Shadow Gun Deadzone](https://res.cloudinary.com/dckoipgrs/image/upload/v1767874500/SCR_Vortex-2_tqsvhn.jpg)

![Walkthrough](https://res.cloudinary.com/dckoipgrs/image/upload/v1767875991/Frame_7-2_v7zt2e.jpg)

> **⚠️ DISCLAIMER**: This tool is for educational purposes only. Using this bot may violate the game's Terms of Service and could result in account suspension or ban. Use at your own risk.

## Overview

An automated currency exchange bot for Shadow Gun Deadzone (Unity game on macOS) that allows players to accumulate unlimited gold and money by exploiting the game's exchange rate mechanics through automated API calls.

##  Features

-  **Fully Automated**: Auto-fetches current player stats from game servers
-  **Smart Resource Management**: Intelligently generates resources even when starting balances are low
-  **Infinite Accumulation**: Uses exchange rate arbitrage to generate unlimited currency
-  **Target-Based**: Simply set your desired gold/money amount and let it run
-  **Safe Rate Limiting**: Configurable delays between requests to avoid detection

##  Technologies Used

### Network Analysis
- **Wireshark** - Packet capture and HTTP traffic analysis
- **HTTP Protocol** - Unencrypted game API communication
- **URL Encoding** - Parameter encoding for API requests

### Development
- **Python 3** - Core automation language
- **requests** library - HTTP client for API calls
- **json** library - JSON parsing and encoding
- **urllib** - URL parameter encoding

### Game Technology
- **Unity Engine** (2021.3.9f1) - Game framework
- **libcurl** - Unity's networking library
- **Apache/PHP Backend** - Game server infrastructure

##  How It Works

### 1. Traffic Interception with Wireshark

The game communicates with its backend server over **unencrypted HTTP**, making it easy to capture and analyze requests.

**Key Endpoints Discovered:**
```
http://shadowgun-comzone.com/sgdz/BuyItem
http://shadowgun-comzone.com/sgdz/getUsrPerProductData
http://shadowgun-comzone.com/sgdz/getCloudDateTime
```

**Example Captured Request:**
```http
POST /sgdz/BuyItem HTTP/1.1
Host: shadowgun-comzone.com
Content-Type: application/x-www-form-urlencoded

param=%7b%22cmd%22%3a%22buyBuiltInItem%22%2c%22prodId%22%3a%22ShadowgunMP%22%2c%22data%22%3a%2245398164%22%2c%22pw%22%3a%22your_password_hash_here%22%2c%22userid%22%3a%22your_userid%22%7d
```

### 2. Request Analysis

**Decoded POST Parameters:**
```json
{
  "cmd": "buyBuiltInItem",
  "prodId": "ShadowgunMP",
  "data": "45398164",
  "pw": "your_password_hash_here",
  "userid": "your_userid"
}
```

**Key Findings:**
- `data`: Item ID for the transaction
  - `45398164` - Buy 250 gold (costs 10,000 money)
  - `1883972191` - Buy 160,000 money (costs 2,000 gold)
- `pw`: MD5 hash of user password (client-side authentication)
- `userid`: Player's unique identifier

### 3. Exchange Rate Arbitrage

**The Exploit:**
```
Exchange Rates:
- 10,000 money → 250 gold
- 2,000 gold → 160,000 money

Arbitrage Cycle:
1. Spend 10k money → Get 250 gold
2. Repeat 8 times → Accumulate 2,000 gold
3. Sell 2,000 gold → Get 160k money
4. Net profit: 80k money (160k - 80k spent)
```

**Result:** Infinite money generation with ~100% ROI per cycle

### 4. Automation Implementation

**Player Data Fetching:**
```python
def get_player_data(self):
    params = {
        "cmd": "getUsrPerProductData",
        "userid": self.userid,
        "prodId": "ShadowgunMP",
        "param": "_PlayerData",
        "pw": self.pw
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return {
        'gold': data['Params']['Gold'],
        'money': data['Params']['Money']
    }
```

**Transaction Execution:**
```python
def buy_item(self, item_data):
    params = {
        "cmd": "buyBuiltInItem",
        "prodId": "ShadowgunMP",
        "data": item_data,
        "pw": self.pw,
        "userid": self.userid
    }
    data = f"param={urllib.parse.quote(json.dumps(params))}"
    response = requests.post(url, headers=headers, data=data)
    return response.text == "ok"
```

## 🚀 Installation

### Prerequisites
```bash
# macOS
brew install python3
```

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/shadowgun-bot.git
cd shadowgun-bot

# Install required dependencies
pip3 install requests
```

##  Usage

### 1. Run the Bot
```bash
python3 shadowgun_bot.py
```

### 2. Enter Credentials

The bot will prompt you to enter your credentials at startup:

```
============================================================
LOGIN CREDENTIALS
============================================================
Enter your User ID: your_userid

Authentication method:
1. Plain password (will be hashed automatically)
2. Password hash (MD5, from Wireshark capture)
Select method (1 or 2): 
```

**Option 1 - Plain Password:**
- Enter your actual game password
- Bot automatically hashes it with MD5
- More convenient for regular use

**Option 2 - Password Hash:**
- Enter the MD5 hash captured from Wireshark
- More secure (password never stored in plaintext)
- Format: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

### 3. Choose Mode

**Option 1: Auto Accumulate Gold**
```
Target GOLD amount: 100000
Delay: 1

✓ Auto-fetches current stats
✓ Calculates optimal strategy
✓ Executes automatically
```

**Option 2: Auto Accumulate Money**
```
Target MONEY amount: 9999999
Delay: 1

✓ Runs infinite money cycles
✓ Reaches any target amount
```

### 4. Finding Your Credentials

**Method 1: Using Wireshark (Recommended)**
1. Start Wireshark packet capture
2. Launch Shadow Gun Deadzone
3. Login to the game
4. Filter: `http.request.uri contains "sgdz"`
5. Find any request with `userid` and `pw` parameters
6. Copy these values

**Method 2: Using Plain Password**
- Simply use your game login password
- Bot will hash it automatically


### Network Protocol Analysis

**Request Structure:**
- Method: `POST`
- Content-Type: `application/x-www-form-urlencoded`
- Authentication: MD5 password hash in payload
- No HTTPS/encryption
- No CSRF tokens
- No rate limiting (initially)

**Response Structure:**
```json
{
  "Params": {
    "Gold": 45806,
    "Money": 9607,
    "Experience": 1768739,
    "Chips": 4
  },
  "InventoryList": {...},
  "Stats": {...}
}
```

### Security Vulnerabilities Exploited

1. **Unencrypted HTTP** - All traffic visible in plaintext
2. **Client-Side Authentication** - Password hash sent with every request
3. **No Server-Side Validation** - Server trusts all item IDs from client
4. **Predictable Item IDs** - Static integers for in-game items
5. **No Rate Limiting** - Unlimited API calls possible
6. **Poor Exchange Rates** - Game mechanics allow infinite arbitrage

##  Performance

- **Speed**: ~1-2 seconds per transaction (configurable)
- **Efficiency**: 100% success rate on valid requests
- **Scalability**: Can accumulate any amount given enough time
- **Detection Risk**: Low (mimics legitimate game traffic)

##  Configuration

### Authentication Options

The bot now supports two authentication methods:

**1. Plain Password (Automatic Hashing)**
```python
bot = ShadowGunBot("your_userid", password="your_password")
```
- Bot automatically hashes with MD5
- More convenient for scripting
- Password not stored anywhere

**2. Pre-captured Password Hash**
```python
bot = ShadowGunBot("your_userid", password_hash="59ef5d7e...")
```
- Use MD5 hash from Wireshark capture
- More secure (no plaintext password)
- Direct API authentication

##  Safety Features

- Configurable delays between requests
- Auto-retry on failed transactions
- Resource validation before execution
- Detailed logging of all operations
- Graceful error handling

##  Use Cases

- **Rapid Progression**: Skip grinding for currency
- **Testing**: Experiment with max-level equipment
- **Research**: Understand game economy mechanics
- **Education**: Learn about API security and exploitation

## ⚠️ Limitations

- Requires at least 10k money OR 2k gold to start cycles
- Execution time scales with target amount due to rate limits
- May trigger anti-cheat if used excessively

##  Ethical Considerations

This project demonstrates:
- The importance of HTTPS/TLS encryption
- Why client-side authentication is dangerous
- The need for server-side validation
- How poor game design can be exploited

**This tool should only be used:**
- On private/offline servers
- For educational purposes
- With explicit permission from game developers
- As a security research demonstration

##  Learning Resources

- [Wireshark Documentation](https://www.wireshark.org/docs/)
- [Python Requests Library](https://docs.python-requests.org/)
- [HTTP Protocol Basics](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [Game Hacking Ethics](https://www.ethicalhacking.com/)

##  Acknowledgments

- Unity Engine for the game framework
- Wireshark team for network analysis tools
- Python community for excellent libraries
- Security researchers who study game vulnerabilities

---

**Remember:** Use responsibly and ethically. This project is for educational purposes only.


For questions or responsible disclosure of security issues:
- GitHub Issues: [Create an issue](https://github.com/yourusername/shadowgun-bot/issues)

