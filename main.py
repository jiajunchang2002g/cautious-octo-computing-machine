
import sqlite3
import json
from datetime import datetime
import mod1  # XRPL wallet functions
import mod2  # Token/currency functions  
import mod3  # NFT functions

class CrowdfundingPlatform:
    def __init__(self):
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for farmer campaigns"""
        conn = sqlite3.connect('crowdfunding.db')
        cursor = conn.cursor()
        
        # Create campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_name TEXT NOT NULL,
                project_title TEXT NOT NULL,
                description TEXT NOT NULL,
                funding_goal INTEGER NOT NULL,
                farmer_wallet_seed TEXT NOT NULL,
                farmer_address TEXT NOT NULL,
                token_currency TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create investments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                investor_address TEXT NOT NULL,
                amount INTEGER NOT NULL,
                token_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")

    def create_campaign(self, farmer_name, project_title, description, funding_goal):
        """Create a new farmer campaign"""
        print(f"\n🚜 Creating campaign for {farmer_name}...")
        
        # Generate XRPL wallet for farmer
        farmer_wallet = mod1.get_account('')
        
        conn = sqlite3.connect('crowdfunding.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO campaigns (farmer_name, project_title, description, funding_goal, 
                                 farmer_wallet_seed, farmer_address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (farmer_name, project_title, description, funding_goal, 
              farmer_wallet.seed, farmer_wallet.address))
        
        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Campaign created with ID: {campaign_id}")
        print(f"   Farmer wallet: {farmer_wallet.address}")
        print(f"   Seed (keep safe): {farmer_wallet.seed}")
        
        return campaign_id

    def approve_campaign(self, campaign_id):
        """Approve campaign and mint project token"""
        conn = sqlite3.connect('crowdfunding.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
        campaign = cursor.fetchone()
        
        if not campaign:
            print("❌ Campaign not found")
            return
            
        farmer_name, project_title = campaign[1], campaign[2]
        farmer_seed = campaign[5]
        
        print(f"\n🎯 Approving campaign: {project_title}")
        
        # Create token currency code (max 3 chars for standard currency)
        token_currency = project_title[:3].upper()
        
        # Configure farmer account for token issuance
        print("   Setting up farmer account...")
        mod2.configure_account(farmer_seed, True)
        
        # Update campaign status and token info
        cursor.execute('''
            UPDATE campaigns SET status = ?, token_currency = ? WHERE id = ?
        ''', ('approved', token_currency, campaign_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Campaign approved! Token currency: {token_currency}")

    def invest_in_campaign(self, campaign_id, investor_seed, investment_amount):
        """Invest XRP in a campaign and receive project tokens"""
        conn = sqlite3.connect('crowdfunding.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM campaigns WHERE id = ? AND status = "approved"', (campaign_id,))
        campaign = cursor.fetchone()
        
        if not campaign:
            print("❌ Campaign not found or not approved")
            return
            
        farmer_seed = campaign[5]
        farmer_address = campaign[6]
        token_currency = campaign[7]
        
        investor_wallet = mod1.get_account(investor_seed)
        
        print(f"\n💰 Processing investment of {investment_amount} XRP...")
        
        # Step 1: Send XRP to farmer
        print("   Sending XRP to farmer...")
        xrp_result = mod1.send_xrp(investor_seed, investment_amount, farmer_address)
        
        if "Submit failed" in str(xrp_result):
            print(f"❌ XRP transfer failed: {xrp_result}")
            return
            
        # Step 2: Create trust line for investor to receive tokens
        print("   Creating trust line for tokens...")
        trust_result = mod2.create_trust_line(investor_seed, farmer_address, token_currency, investment_amount * 10)
        
        # Step 3: Send project tokens to investor
        print("   Sending project tokens...")
        token_amount = investment_amount  # 1:1 ratio for MVP
        token_result = mod2.send_currency(farmer_seed, investor_wallet.address, token_currency, token_amount)
        
        # Record investment
        cursor.execute('''
            INSERT INTO investments (campaign_id, investor_address, amount)
            VALUES (?, ?, ?)
        ''', (campaign_id, investor_wallet.address, investment_amount))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Investment successful!")
        print(f"   Received {token_amount} {token_currency} tokens")

    def list_campaigns(self):
        """List all campaigns"""
        conn = sqlite3.connect('crowdfunding.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM campaigns ORDER BY created_at DESC')
        campaigns = cursor.fetchall()
        
        print("\n📋 All Campaigns:")
        print("-" * 80)
        
        for campaign in campaigns:
            campaign_id, farmer_name, title, desc, goal, _, _, token, status, created = campaign
            print(f"ID: {campaign_id} | {title} by {farmer_name}")
            print(f"   Goal: {goal} XRP | Status: {status} | Token: {token or 'N/A'}")
            print(f"   Description: {desc}")
            print(f"   Created: {created}")
            print("-" * 80)
            
        conn.close()

    def check_balances(self, wallet_seed):
        """Check wallet balances"""
        wallet = mod1.get_account(wallet_seed)
        print(f"\n💼 Wallet: {wallet.address}")
        
        # Get XRP balance
        account_info = mod1.get_account_info(wallet.address)
        xrp_balance = int(account_info['Balance']) / 1000000  # Convert drops to XRP
        print(f"   XRP Balance: {xrp_balance} XRP")
        
        # Get token balances
        balance_info = mod2.get_balance(wallet_seed, wallet_seed)
        if 'balances' in balance_info:
            print("   Token Balances:")
            for currency, amount in balance_info['balances'].items():
                print(f"     {currency}: {amount}")

def main():
    platform = CrowdfundingPlatform()
    
    while True:
        print("\n🌾 FARMER CROWDFUNDING PLATFORM 🌾")
        print("1. Create Campaign")
        print("2. List Campaigns") 
        print("3. Approve Campaign (Admin)")
        print("4. Invest in Campaign")
        print("5. Check Wallet Balance")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            farmer_name = input("Farmer name: ")
            project_title = input("Project title: ")
            description = input("Project description: ")
            funding_goal = int(input("Funding goal (XRP): "))
            platform.create_campaign(farmer_name, project_title, description, funding_goal)
            
        elif choice == "2":
            platform.list_campaigns()
            
        elif choice == "3":
            campaign_id = int(input("Campaign ID to approve: "))
            platform.approve_campaign(campaign_id)
            
        elif choice == "4":
            campaign_id = int(input("Campaign ID to invest in: "))
            investor_seed = input("Your wallet seed (or press Enter for new wallet): ").strip()
            if not investor_seed:
                new_wallet = mod1.get_account('')
                investor_seed = new_wallet.seed
                print(f"New wallet created: {new_wallet.address}")
                print(f"Your seed (save this!): {investor_seed}")
            
            amount = int(input("Investment amount (XRP): "))
            platform.invest_in_campaign(campaign_id, investor_seed, amount)
            
        elif choice == "5":
            wallet_seed = input("Wallet seed: ")
            platform.check_balances(wallet_seed)
            
        elif choice == "6":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()
