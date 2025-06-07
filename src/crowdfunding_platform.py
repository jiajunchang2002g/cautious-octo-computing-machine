import json
import os
from datetime import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mods'))
import wallet  # XRPL wallet functions
import tokens  # Token/currency functions
import escrow_time  # Time-based escrow functions  

class CrowdfundingPlatform:
    def __init__(self):
        self.storage_file = os.path.join('storage', 'storage.json')
        self.init_storage()
        
    def init_storage(self):
        """Initialize JSON storage for campaigns and investments"""
        if not os.path.exists(self.storage_file):
            initial_data = {
                'campaigns': [],
                'investments': [],
                'next_campaign_id': 1,
                'next_investment_id': 1
            }
            with open(self.storage_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
            print("✅ Storage initialized")
        else:
            print("✅ Storage loaded")

    def load_data(self):
        """Load data from JSON file"""
        with open(self.storage_file, 'r') as f:
            return json.load(f)

    def save_data(self, data):
        """Save data to JSON file"""
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)

    def create_campaign(self, farmer_name, project_title, description, funding_goal):
        """Create a new farmer campaign"""
        print(f"\n🚜 Creating campaign for {farmer_name}...")
        
        # Generate XRPL wallet for farmer
        farmer_wallet = wallet.get_account('')
        
        data = self.load_data()
        
        campaign = {
            'id': data['next_campaign_id'],
            'farmer_name': farmer_name,
            'project_title': project_title,
            'description': description,
            'funding_goal': funding_goal,
            'farmer_wallet_seed': farmer_wallet.seed,
            'farmer_address': farmer_wallet.address,
            'token_currency': None,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        data['campaigns'].append(campaign)
        data['next_campaign_id'] += 1
        self.save_data(data)
        
        campaign_id = campaign['id']
        print(f"✅ Campaign created with ID: {campaign_id}")
        print(f"   Farmer wallet: {farmer_wallet.address}")
        print(f"   Seed (keep safe): {farmer_wallet.seed}")
        
        return campaign_id

    def approve_campaign(self, campaign_id):
        """Approve campaign and mint project token"""
        data = self.load_data()
        
        campaign = None
        for c in data['campaigns']:
            if c['id'] == campaign_id:
                campaign = c
                break
        
        if not campaign:
            print("❌ Campaign not found")
            return
            
        farmer_name = campaign['farmer_name']
        project_title = campaign['project_title']
        farmer_seed = campaign['farmer_wallet_seed']
        
        print(f"\n🎯 Approving campaign: {project_title}")
        
        # Create token currency code (max 3 chars for standard currency)
        token_currency = project_title[:3].upper()
        
        # Configure farmer account for token issuance
        print("   Setting up farmer account...")
        tokens.configure_account(farmer_seed, True)
        
        # Update campaign status and token info
        campaign['status'] = 'approved'
        campaign['token_currency'] = token_currency
        
        self.save_data(data)
        
        print(f"✅ Campaign approved! Token currency: {token_currency}")

    def invest_in_campaign(self, campaign_id, investor_seed, investment_amount):
        """Invest XRP in a campaign and receive project tokens"""
        data = self.load_data()
        
        campaign = None
        for c in data['campaigns']:
            if c['id'] == campaign_id and c['status'] == 'approved':
                campaign = c
                break
        
        if not campaign:
            print("❌ Campaign not found or not approved")
            return
            
        farmer_seed = campaign['farmer_wallet_seed']
        farmer_address = campaign['farmer_address']
        token_currency = campaign['token_currency']
        
        investor_wallet = wallet.get_account(investor_seed)
        
        print(f"\n💰 Processing investment of {investment_amount} XRP...")
        
        # Step 1: Send XRP to farmer
        print("   Sending XRP to farmer...")
        xrp_result = wallet.send_xrp(investor_seed, investment_amount, farmer_address)
        
        if "Submit failed" in str(xrp_result):
            print(f"❌ XRP transfer failed: {xrp_result}")
            return
            
        # Step 2: Create trust line for investor to receive tokens
        print("   Creating trust line for tokens...")
        trust_result = tokens.create_trust_line(investor_seed, farmer_address, token_currency, investment_amount * 10)
        
        # Step 3: Send project tokens to investor
        print("   Sending project tokens...")
        token_amount = investment_amount  # 1:1 ratio for MVP
        token_result = tokens.send_currency(farmer_seed, investor_wallet.address, token_currency, token_amount)
        
        # Record investment
        investment = {
            'id': data['next_investment_id'],
            'campaign_id': campaign_id,
            'investor_address': investor_wallet.address,
            'amount': investment_amount,
            'token_id': None,
            'created_at': datetime.now().isoformat()
        }
        
        data['investments'].append(investment)
        data['next_investment_id'] += 1
        self.save_data(data)
        
        print(f"✅ Investment successful!")
        print(f"   Received {token_amount} {token_currency} tokens")

    def list_campaigns(self):
        """List all campaigns"""
        data = self.load_data()
        campaigns = data['campaigns']
        
        print("\n📋 All Campaigns:")
        print("-" * 80)
        
        if not campaigns:
            print("No campaigns found.")
            return
        
        for campaign in sorted(campaigns, key=lambda x: x['created_at'], reverse=True):
            campaign_id = campaign['id']
            farmer_name = campaign['farmer_name']
            title = campaign['project_title']
            desc = campaign['description']
            goal = campaign['funding_goal']
            token = campaign['token_currency']
            status = campaign['status']
            created = campaign['created_at']
            
            print(f"ID: {campaign_id} | {title} by {farmer_name}")
            print(f"   Goal: {goal} XRP | Status: {status} | Token: {token or 'N/A'}")
            print(f"   Description: {desc}")
            print(f"   Created: {created}")
            print("-" * 80)

    def create_microloan(self, farmer_address, investor_seed, loan_amount, repayment_days):
        """Create an escrow-based microloan"""
        print(f"\n🏦 Creating microloan of {loan_amount} XRP...")
        
        # Convert loan amount to drops (XRP smallest unit)
        loan_amount_drops = str(int(loan_amount * 1000000))
        
        # Calculate time periods (in seconds)
        repayment_seconds = repayment_days * 24 * 60 * 60
        cancel_seconds = repayment_seconds + (7 * 24 * 60 * 60)  # 7 days grace period
        
        # Create time-based escrow
        print("   Creating escrow contract...")
        escrow_result = escrow_time.create_time_escrow(
            investor_seed,
            loan_amount_drops,
            farmer_address,
            repayment_seconds,
            cancel_seconds
        )
        
        if "Submit failed" in str(escrow_result):
            print(f"❌ Escrow creation failed: {escrow_result}")
            return None
            
        # Store microloan data
        data = self.load_data()
        
        if 'microloans' not in data:
            data['microloans'] = []
            data['next_microloan_id'] = 1
        
        investor_wallet = wallet.get_account(investor_seed)
        
        microloan = {
            'id': data['next_microloan_id'],
            'farmer_address': farmer_address,
            'investor_address': investor_wallet.address,
            'loan_amount': loan_amount,
            'repayment_days': repayment_days,
            'status': 'active',
            'escrow_sequence': escrow_result.get('Sequence', 0),
            'created_at': datetime.now().isoformat()
        }
        
        data['microloans'].append(microloan)
        data['next_microloan_id'] += 1
        self.save_data(data)
        
        print(f"✅ Microloan created!")
        print(f"   Loan ID: {microloan['id']}")
        print(f"   Amount: {loan_amount} XRP")
        print(f"   Repayment due: {repayment_days} days")
        print(f"   Escrow sequence: {microloan['escrow_sequence']}")
        
        return microloan['id']

    def finish_microloan(self, microloan_id, farmer_seed):
        """Finish microloan escrow (farmer claims funds)"""
        data = self.load_data()
        
        microloan = None
        for ml in data.get('microloans', []):
            if ml['id'] == microloan_id and ml['status'] == 'active':
                microloan = ml
                break
        
        if not microloan:
            print("❌ Microloan not found or already completed")
            return
            
        print(f"\n💰 Finishing microloan #{microloan_id}...")
        
        # Farmer claims the escrowed funds
        finish_result = escrow_time.finish_time_escrow(
            farmer_seed,
            microloan['investor_address'],
            microloan['escrow_sequence']
        )
        
        if "Submit failed" in str(finish_result):
            print(f"❌ Escrow finish failed: {finish_result}")
            return
            
        # Update microloan status
        microloan['status'] = 'completed'
        microloan['completed_at'] = datetime.now().isoformat()
        self.save_data(data)
        
        print(f"✅ Microloan completed! Farmer received {microloan['loan_amount']} XRP")

    def cancel_microloan(self, microloan_id, investor_seed):
        """Cancel microloan escrow (investor reclaims funds)"""
        data = self.load_data()
        
        microloan = None
        for ml in data.get('microloans', []):
            if ml['id'] == microloan_id and ml['status'] == 'active':
                microloan = ml
                break
        
        if not microloan:
            print("❌ Microloan not found or already completed")
            return
            
        print(f"\n🔄 Canceling microloan #{microloan_id}...")
        
        # Investor reclaims the escrowed funds
        cancel_result = escrow_time.cancel_time_escrow(
            investor_seed,
            microloan['investor_address'],
            microloan['escrow_sequence']
        )
        
        if "Submit failed" in str(cancel_result):
            print(f"❌ Escrow cancel failed: {cancel_result}")
            return
            
        # Update microloan status
        microloan['status'] = 'cancelled'
        microloan['cancelled_at'] = datetime.now().isoformat()
        self.save_data(data)
        
        print(f"✅ Microloan cancelled! Investor reclaimed {microloan['loan_amount']} XRP")

    def list_microloans(self):
        """List all microloans"""
        data = self.load_data()
        microloans = data.get('microloans', [])
        
        print("\n🏦 All Microloans:")
        print("-" * 80)
        
        if not microloans:
            print("No microloans found.")
            return
        
        for loan in sorted(microloans, key=lambda x: x['created_at'], reverse=True):
            loan_id = loan['id']
            farmer = loan['farmer_address'][:10] + "..."
            investor = loan['investor_address'][:10] + "..."
            amount = loan['loan_amount']
            days = loan['repayment_days']
            status = loan['status']
            created = loan['created_at']
            
            print(f"ID: {loan_id} | {amount} XRP | {days} days | Status: {status}")
            print(f"   Farmer: {farmer} | Investor: {investor}")
            print(f"   Created: {created}")
            print("-" * 80)

    def check_balances(self, wallet_seed):
        """Check wallet balances"""
        user_wallet = wallet.get_account(wallet_seed)
        print(f"\n💼 Wallet: {user_wallet.address}")
        
        # Get XRP balance
        account_info = wallet.get_account_info(user_wallet.address)
        xrp_balance = int(account_info['Balance']) / 1000000  # Convert drops to XRP
        print(f"   XRP Balance: {xrp_balance} XRP")
        
        # Get token balances
        balance_info = tokens.get_balance(wallet_seed, wallet_seed)
        if 'balances' in balance_info:
            print("   Token Balances:")
            for currency, amount in balance_info['balances'].items():
                print(f"     {currency}: {amount}")
