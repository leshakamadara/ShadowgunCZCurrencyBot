#!/usr/bin/env python3
"""
Shadow Gun Deadzone - Currency Exchange Automation
WARNING: This may violate the game's Terms of Service and could result in account ban.
Use at your own risk.
"""

import requests
import json
import time
import urllib.parse
import hashlib

class ShadowGunBot:
    def __init__(self, userid, password=None, password_hash=None):
        """
        Initialize bot with credentials.
        
        Args:
            userid: User ID from game
            password: Plain text password (will be hashed with MD5)
            password_hash: Pre-captured MD5 hash of password
            
        Note: Provide either password OR password_hash, not both.
        """
        self.base_url = "http://shadowgun-comzone.com"
        self.userid = userid
        
        # Accept either password or password_hash
        if password_hash:
            self.pw = password_hash
        elif password:
            # Hash the password using MD5
            self.pw = hashlib.md5(password.encode()).hexdigest()
        else:
            raise ValueError("Must provide either 'password' or 'password_hash'")
        self.headers = {
            'User-Agent': 'UnityPlayer/2021.3.9f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'Accept-Encoding': 'deflate, gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Unity-Version': '2021.3.9f1'
        }
        
        # Item IDs from captured traffic
        self.ITEM_BUY_MONEY = "1883972191"  # 160k money for 2k gold
        self.ITEM_BUY_GOLD = "45398164"     # 250 gold for 10k money
    
    def get_server_time(self):
        """Get server time (optional, for verification)"""
        params = {
            "cmd": "getCloudDateTime",
            "userid": self.userid,
            "pw": self.pw
        }
        
        url = f"{self.base_url}/sgdz/getCloudDateTime?param={urllib.parse.quote(json.dumps(params))}"
        
        try:
            response = requests.get(url, headers=self.headers)
            print(f"Server time response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error getting server time: {e}")
            return None
    
    def get_player_data(self):
        """Fetch current player data including gold and money"""
        params = {
            "cmd": "getUsrPerProductData",
            "userid": self.userid,
            "prodId": "ShadowgunMP",
            "param": "_PlayerData",
            "pw": self.pw
        }
        
        url = f"{self.base_url}/sgdz/getUsrPerProductData?param={urllib.parse.quote(json.dumps(params))}"
        
        try:
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            # The gold and money are nested under "Params"
            if 'Params' in data:
                params_data = data['Params']
                return {
                    'gold': int(params_data.get('Gold', 0)),
                    'money': int(params_data.get('Money', 0)),
                    'experience': int(params_data.get('Experience', 0)),
                    'chips': int(params_data.get('Chips', 0))
                }
            else:
                print(f"✗ Unexpected response structure")
                print(f"Response keys: {data.keys()}")
                return None
                
        except Exception as e:
            print(f"Error getting player data: {e}")
            return None
    
    def buy_item(self, item_data):
        """Execute a buy transaction"""
        params = {
            "cmd": "buyBuiltInItem",
            "prodId": "ShadowgunMP",
            "data": item_data,
            "pw": self.pw,
            "userid": self.userid
        }
        
        # URL encode the parameters
        data = f"param={urllib.parse.quote(json.dumps(params))}"
        
        url = f"{self.base_url}/sgdz/BuyItem"
        
        try:
            response = requests.post(url, headers=self.headers, data=data)
            print(f"Response: {response.text}")
            return response.text == "ok"
        except Exception as e:
            print(f"Error buying item: {e}")
            return False
    
    def buy_gold(self, count=1, delay=1.0):
        """Buy gold with money (250 gold for 10k money)"""
        print(f"\n=== Buying Gold {count} times ===")
        print(f"Cost: {count * 10000} money")
        print(f"Gain: {count * 250} gold")
        
        success_count = 0
        for i in range(count):
            print(f"\n[{i+1}/{count}] Buying 250 gold...")
            if self.buy_item(self.ITEM_BUY_GOLD):
                success_count += 1
                print(f"✓ Success! ({success_count}/{count})")
            else:
                print(f"✗ Failed!")
            
            if i < count - 1:  # Don't sleep after last iteration
                time.sleep(delay)
        
        print(f"\n=== Complete: {success_count}/{count} successful ===")
        return success_count
    
    def buy_money(self, count=1, delay=1.0):
        """Buy money with gold (160k money for 2k gold)"""
        print(f"\n=== Buying Money {count} times ===")
        print(f"Cost: {count * 2000} gold")
        print(f"Gain: {count * 160000} money")
        
        success_count = 0
        for i in range(count):
            print(f"\n[{i+1}/{count}] Buying 160k money...")
            if self.buy_item(self.ITEM_BUY_MONEY):
                success_count += 1
                print(f"✓ Success! ({success_count}/{count})")
            else:
                print(f"✗ Failed!")
            
            if i < count - 1:
                time.sleep(delay)
        
        print(f"\n=== Complete: {success_count}/{count} successful ===")
        return success_count
    
    def convert_all_money_to_gold(self, total_money, delay=1.0):
        """Convert all available money to gold"""
        transactions_needed = total_money // 10000
        print(f"\nYou have {total_money} money")
        print(f"Can buy gold {transactions_needed} times")
        print(f"Will get {transactions_needed * 250} gold")
        
        confirm = input("\nProceed? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
        
        self.buy_gold(transactions_needed, delay)
    
    def accumulate_gold(self, current_money, current_gold, target_gold, delay=1.0):
        """Accumulate gold to reach target amount"""
        print(f"\n{'='*60}")
        print(f"GOLD ACCUMULATION PLAN")
        print(f"{'='*60}")
        print(f"Current: {current_gold} gold, {current_money} money")
        print(f"Target:  {target_gold} gold")
        
        gold_needed = target_gold - current_gold
        
        if gold_needed <= 0:
            print(f"\n✓ You already have {current_gold} gold (target: {target_gold})")
            return
        
        print(f"Need:    {gold_needed} more gold")
        
        # Calculate transactions needed (250 gold per transaction)
        transactions_needed = (gold_needed + 249) // 250  # Round up
        gold_will_get = transactions_needed * 250
        money_needed = transactions_needed * 10000
        
        print(f"\nPlan:")
        print(f"  - Buy gold {transactions_needed} times")
        print(f"  - Will get {gold_will_get} gold")
        print(f"  - Costs {money_needed} money")
        print(f"  - Final gold: {current_gold + gold_will_get}")
        
        # Check if we have enough money
        if current_money < money_needed:
            money_shortage = money_needed - current_money
            print(f"\n⚠ Not enough money! Need {money_shortage} more")
            
            # Strategy: Use money cycles to generate more money first
            # Each cycle: 10k money → 250 gold → 20k money (net +10k)
            print(f"\nSolution: Generate money first using cycles")
            
            # We need at least 10k to start a cycle
            if current_money < 10000:
                # Need to sell some gold to get 10k
                gold_to_sell = 1  # Sell 2000 gold for 160k money
                if current_gold < 2000:
                    print(f"\n✗ Cannot start: Need at least 2000 gold OR 10k money")
                    print(f"  You have: {current_gold} gold, {current_money} money")
                    return
                
                print(f"  Step 0: Sell 2000 gold → Get 160k money")
                current_money += 160000  # Will have this after step 0
                current_gold -= 2000
            
            # Calculate how many cycles to run to get enough money
            cycles_for_money = (money_shortage + 9999) // 10000
            
            print(f"  Step 1: Run {cycles_for_money} money cycles → Get ~{cycles_for_money * 10000} money")
            print(f"  Step 2: Buy gold {transactions_needed} times → Get {gold_will_get} gold")
            
            print("\n⏳ Starting execution in 3 seconds...")
            time.sleep(3)
            
            # Step 0: Get starting money if needed
            if current_money < 10000:
                print(f"\n{'='*60}")
                print(f"STEP 0: Getting starting money")
                print(f"{'='*60}")
                self.buy_money(1, delay)
            
            # Step 1: Run money cycles
            print(f"\n{'='*60}")
            print(f"STEP 1: Generating money via cycles")
            print(f"{'='*60}")
            
            for i in range(cycles_for_money):
                print(f"\n[Cycle {i+1}/{cycles_for_money}]")
                print(f"  → Buy 250 gold (10k money)...")
                if not self.buy_item(self.ITEM_BUY_GOLD):
                    print(f"  ✗ Failed!")
                    continue
                
                # Every 8 cycles, sell accumulated gold
                if (i + 1) % 8 == 0:
                    print(f"  → Sell 2000 gold (160k money)...")
                    if not self.buy_item(self.ITEM_BUY_MONEY):
                        print(f"  ✗ Failed!")
                
                time.sleep(delay)
            
            # Sell remaining gold
            remaining_cycles = cycles_for_money % 8
            if remaining_cycles > 0:
                accumulated_gold = remaining_cycles * 250
                if accumulated_gold >= 2000:
                    times = accumulated_gold // 2000
                    print(f"\n[Final] Selling {accumulated_gold} gold...")
                    self.buy_money(times, delay)
            
            # Step 2: Now buy the target gold
            print(f"\n{'='*60}")
            print(f"STEP 2: Buying target gold")
            print(f"{'='*60}")
            self.buy_gold(transactions_needed, delay)
            
        else:
            # We have enough money, just buy gold
            print(f"\n✓ You have enough money: {current_money} / {money_needed}")
            
            print("\n⏳ Starting execution in 3 seconds...")
            time.sleep(3)
            
            self.buy_gold(transactions_needed, delay)
    
    def accumulate_money(self, current_money, current_gold, target_money, delay=1.0):
        """Accumulate money to reach target amount"""
        print(f"\n{'='*60}")
        print(f"MONEY ACCUMULATION PLAN")
        print(f"{'='*60}")
        print(f"Current: {current_money} money, {current_gold} gold")
        print(f"Target:  {target_money} money")
        
        money_needed = target_money - current_money
        
        if money_needed <= 0:
            print(f"\n✓ You already have {current_money} money (target: {target_money})")
            return
        
        print(f"Need:    {money_needed} more money")
        
        # Strategy: Use money→gold→money cycles for infinite money generation
        # Each cycle: 10k money → 250 gold → 20k money (net +10k money)
        
        print(f"\nStrategy: Money multiplication cycles")
        print(f"  Each cycle: 10k money → 250 gold → 20k money")
        print(f"  Net gain: +10k money per cycle")
        
        # Calculate how many cycles we need
        cycles_needed = (money_needed + 9999) // 10000  # Round up
        
        # Check if we have the initial 10k to start
        if current_money < 10000:
            # We need to convert some gold to get started
            gold_to_convert = ((10000 - current_money) + 159999) // 160000  # Round up
            if current_gold < gold_to_convert * 2000:
                print(f"\n✗ IMPOSSIBLE: Need at least {gold_to_convert * 2000} gold to start")
                print(f"  You have: {current_gold} gold")
                return
            
            print(f"\nStep 0: Get starting money")
            print(f"  - Convert {gold_to_convert}x gold → Get {gold_to_convert * 160000} money")
            print(f"  - Costs {gold_to_convert * 2000} gold")
            
            print(f"\nStep 1: Run {cycles_needed} money cycles")
            print(f"  - Total transactions: {cycles_needed * 2}")
            print(f"  - Final money: ~{current_money + gold_to_convert * 160000 + cycles_needed * 10000}")
            
            print("\n⏳ Starting execution in 3 seconds...")
            time.sleep(3)
            
            # Get starting money
            print(f"\n{'='*60}")
            print(f"STEP 0: Getting starting money")
            print(f"{'='*60}")
            self.buy_money(gold_to_convert, delay)
            
        else:
            # We have enough to start cycles
            print(f"\nPlan: Run {cycles_needed} cycles")
            print(f"  - Starting with {current_money} money")
            print(f"  - Total transactions: {cycles_needed * 2}")
            print(f"  - Final money: ~{current_money + cycles_needed * 10000}")
            
            print("\n⏳ Starting execution in 3 seconds...")
            time.sleep(3)
        
        # Execute cycles
        print(f"\n{'='*60}")
        print(f"RUNNING MONEY CYCLES")
        print(f"{'='*60}")
        
        for i in range(cycles_needed):
            print(f"\n[Cycle {i+1}/{cycles_needed}]")
            
            # Step 1: Buy 250 gold with 10k money
            print(f"  → Buying 250 gold (costs 10k money)...")
            if not self.buy_item(self.ITEM_BUY_GOLD):
                print(f"  ✗ Failed to buy gold!")
                continue
            
            # Step 2: Sell 250 gold (but we need 2000 gold for one transaction)
            # We need to accumulate gold over 8 cycles, then sell
            # Actually, let's sell immediately using partial gold
            # Wait, we can't sell 250 gold directly - minimum is 2000 gold for 160k money
            
            # Better strategy: accumulate 8 buys (8 * 250 = 2000 gold), then sell once
            if (i + 1) % 8 == 0:  # Every 8 cycles
                print(f"  → Selling 2000 gold (gets 160k money)...")
                if not self.buy_item(self.ITEM_BUY_MONEY):
                    print(f"  ✗ Failed to sell gold!")
            
            if i < cycles_needed - 1:
                time.sleep(delay)
        
        # Sell any remaining gold
        remaining_gold = (cycles_needed % 8) * 250
        if remaining_gold >= 2000:
            times = remaining_gold // 2000
            print(f"\n[Final] Selling remaining {remaining_gold} gold...")
            self.buy_money(times, delay)
    
    def auto_accumulate_gold(self, target_gold, delay=1.0):
        """Automatically fetch current stats and accumulate gold"""
        print(f"\n{'='*60}")
        print(f"AUTO GOLD ACCUMULATION")
        print(f"{'='*60}")
        print("Fetching current player data...")
        
        player_data = self.get_player_data()
        
        if not player_data:
            print("✗ Failed to fetch player data. Please try manual mode.")
            return
        
        current_gold = player_data['gold']
        current_money = player_data['money']
        
        print(f"✓ Current stats retrieved:")
        print(f"  Gold: {current_gold}")
        print(f"  Money: {current_money}")
        
        self.accumulate_gold(current_money, current_gold, target_gold, delay)
    
    def auto_accumulate_money(self, target_money, delay=1.0):
        """Automatically fetch current stats and accumulate money"""
        print(f"\n{'='*60}")
        print(f"AUTO MONEY ACCUMULATION")
        print(f"{'='*60}")
        print("Fetching current player data...")
        
        player_data = self.get_player_data()
        
        if not player_data:
            print("✗ Failed to fetch player data. Please try manual mode.")
            return
        
        current_money = player_data['money']
        current_gold = player_data['gold']
        
        print(f"✓ Current stats retrieved:")
        print(f"  Money: {current_money}")
        print(f"  Gold: {current_gold}")
        
        self.accumulate_money(current_money, current_gold, target_money, delay)


# ======================
# USAGE EXAMPLES
# ======================

def main():
    print("=" * 60)
    print("Shadow Gun Deadzone - Currency Exchange Bot")
    print("=" * 60)
    print("\nWARNING: This may violate ToS and result in account ban!")
    
    # Prompt for credentials
    print("\n" + "=" * 60)
    print("LOGIN CREDENTIALS")
    print("=" * 60)
    
    USERID = input("Enter your User ID: ").strip()
    
    print("\nAuthentication method:")
    print("1. Plain password (will be hashed automatically)")
    print("2. Password hash (MD5, from Wireshark capture)")
    
    auth_choice = input("Select method (1 or 2): ").strip()
    
    if auth_choice == "1":
        PASSWORD = input("Enter your password: ").strip()
        bot = ShadowGunBot(USERID, password=PASSWORD)
    elif auth_choice == "2":
        PASSWORD_HASH = input("Enter your password hash: ").strip()
        bot = ShadowGunBot(USERID, password_hash=PASSWORD_HASH)
    else:
        print("Invalid choice! Exiting...")
        return
    
    print("\n✓ Credentials loaded successfully!")
    print("\nOptions:")
    print("1. AUTO: Accumulate GOLD to target (fetches current stats)")
    print("2. AUTO: Accumulate MONEY to target (fetches current stats)")
    print("3. Manual: Accumulate GOLD (you enter current stats)")
    print("4. Manual: Accumulate MONEY (you enter current stats)")
    print("5. Manual: Buy gold (250 gold for 10k money)")
    print("6. Manual: Buy money (160k money for 2k gold)")
    print("7. Test: Fetch current player stats")
    print("8. Exit")
    
    while True:
        choice = input("\nSelect option (1-8): ")
        
        if choice == "1":
            target_gold = int(input("Target GOLD amount: "))
            delay = float(input("Delay between requests (0.5-2 recommended): "))
            bot.auto_accumulate_gold(target_gold, delay)
            
        elif choice == "2":
            target_money = int(input("Target MONEY amount: "))
            delay = float(input("Delay between requests (0.5-2 recommended): "))
            bot.auto_accumulate_money(target_money, delay)
            
        elif choice == "3":
            print("\n" + "=" * 60)
            current_gold = int(input("Current GOLD: "))
            current_money = int(input("Current MONEY: "))
            target_gold = int(input("Target GOLD: "))
            delay = float(input("Delay (0.5-2 recommended): "))
            bot.accumulate_gold(current_money, current_gold, target_gold, delay)
            
        elif choice == "4":
            print("\n" + "=" * 60)
            current_money = int(input("Current MONEY: "))
            current_gold = int(input("Current GOLD: "))
            target_money = int(input("Target MONEY: "))
            delay = float(input("Delay (0.5-2 recommended): "))
            bot.accumulate_money(current_money, current_gold, target_money, delay)
            
        elif choice == "5":
            count = int(input("How many times to buy gold? "))
            delay = float(input("Delay between requests (seconds): "))
            bot.buy_gold(count, delay)
            
        elif choice == "6":
            count = int(input("How many times to buy money? "))
            delay = float(input("Delay between requests (seconds): "))
            bot.buy_money(count, delay)
            
        elif choice == "7":
            print("\nFetching player data...")
            data = bot.get_player_data()
            if data:
                print(f"\n✓ Success!")
                print(f"  Gold: {data['gold']}")
                print(f"  Money: {data['money']}")
            else:
                print("\n✗ Failed to fetch data")
                print("The response structure might be different than expected.")
                print("Try capturing the getUsrPerProductData response in Wireshark")
                print("and share it so we can parse it correctly.")
            
        elif choice == "8":
            print("Exiting...")
            break
        
        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()