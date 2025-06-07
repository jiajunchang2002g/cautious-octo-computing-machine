import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mods'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import wallet
from crowdfunding_platform import CrowdfundingPlatform

def display_menu():
    """Display the main menu"""
    print("\n🌾 FARMER CROWDFUNDING PLATFORM 🌾")
    print("1. Create Campaign")
    print("2. List Campaigns") 
    print("3. Approve Campaign (Admin)")
    print("4. Invest in Campaign")
    print("5. Create Microloan")
    print("6. List Microloans")
    print("7. Claim Microloan (Farmer)")
    print("8. Cancel Microloan (Investor)")
    print("9. Check Wallet Balance")
    print("10. Clear Storage (Admin)")
    print("11. Exit")

def handle_create_campaign(platform):
    """Handle campaign creation"""
    farmer_name = input("Farmer name: ")
    project_title = input("Project title: ")
    description = input("Project description: ")
    funding_goal = int(input("Funding goal (XRP): "))
    platform.create_campaign(farmer_name, project_title, description, funding_goal)

def handle_approve_campaign(platform):
    """Handle campaign approval"""
    campaign_id = int(input("Campaign ID to approve: "))
    platform.approve_campaign(campaign_id)

def handle_investment(platform):
    """Handle investment in campaign"""
    campaign_id = int(input("Campaign ID to invest in: "))
    investor_seed = input("Your wallet seed (or press Enter for new wallet): ").strip()
    if not investor_seed:
        new_wallet = wallet.get_account('')
        investor_seed = new_wallet.seed
        print(f"New wallet created: {new_wallet.address}")
        print(f"Your seed (save this!): {investor_seed}")

    amount = int(input("Investment amount (XRP): "))
    platform.invest_in_campaign(campaign_id, investor_seed, amount)

def handle_check_balance(platform):
    """Handle balance checking"""
    wallet_seed = input("Wallet seed: ")
    platform.check_balances(wallet_seed)

def cli_handle():
    """Main CLI handler"""
    platform = CrowdfundingPlatform()

    while True:
        display_menu()
        choice = input("\nSelect option (1-11): ").strip()

        if choice == "1":
            handle_create_campaign(platform)
        elif choice == "2":
            platform.list_campaigns()
        elif choice == "3":
            handle_approve_campaign(platform)
        elif choice == "4":
            handle_investment(platform)
        elif choice == "5":
            handle_create_microloan(platform)
        elif choice == "6":
            platform.list_microloans()
        elif choice == "7":
            handle_claim_microloan(platform)
        elif choice == "8":
            handle_cancel_microloan(platform)
        elif choice == "9":
            handle_check_balance(platform)
        elif choice == "10":
            handle_clear_storage(platform)
        elif choice == "11":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

def handle_create_microloan(platform):
    """Handle microloan creation"""
    farmer_address = input("Farmer wallet address: ")
    investor_seed = input("Investor wallet seed: ")
    amount = int(input("Loan amount (XRP): "))
    repayment_days = int(input("Repayment period (days): "))
    platform.create_microloan(farmer_address, investor_seed, amount, repayment_days)

def handle_claim_microloan(platform):
    """Handle microloan claiming"""
    microloan_id = int(input("Microloan ID to claim: "))
    farmer_seed = input("Farmer wallet seed: ")
    platform.finish_microloan(microloan_id, farmer_seed)

def handle_cancel_microloan(platform):
    """Handle microloan cancellation"""
    microloan_id = int(input("Microloan ID to cancel: "))
    investor_seed = input("Investor wallet seed: ")
    platform.cancel_microloan(microloan_id, investor_seed)

def handle_clear_storage(platform):
    """Handle storage clearing"""
    confirm = input("⚠️  This will delete ALL campaigns, investments, and microloans. Type 'CONFIRM' to proceed: ")
    if confirm == "CONFIRM":
        platform.clear_storage()
    else:
        print("❌ Storage clear cancelled.")