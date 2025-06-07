
#!/usr/bin/env python3
"""
Test script for escrow functionality
Tests both time-based and conditional escrows
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'mods'))

import wallet
import escrow_time
import escrow_conditional
from datetime import datetime

def test_time_escrow():
    """Test time-based escrow creation and operations"""
    print("\n=== TESTING TIME-BASED ESCROW ===")
    
    # Create and fund wallets
    print("1. Creating investor and farmer wallets...")
    investor_wallet = wallet.get_account('')  # Empty seed = new funded wallet
    farmer_wallet = wallet.get_account('')
    
    print(f"   Investor: {investor_wallet.address}")
    print(f"   Farmer: {farmer_wallet.address}")
    
    # Check balances
    print("2. Checking initial balances...")
    try:
        investor_info = wallet.get_account_info(investor_wallet.address)
        investor_balance = int(investor_info['Balance']) / 1000000
        print(f"   Investor XRP balance: {investor_balance} XRP")
        
        farmer_info = wallet.get_account_info(farmer_wallet.address)
        farmer_balance = int(farmer_info['Balance']) / 1000000
        print(f"   Farmer XRP balance: {farmer_balance} XRP")
    except Exception as e:
        print(f"   Error checking balances: {e}")
        return
    
    # Create escrow
    print("3. Creating time-based escrow...")
    loan_amount = 5  # XRP
    loan_amount_drops = str(int(loan_amount * 1000000))
    finish_seconds = 60  # 1 minute
    cancel_seconds = 300  # 5 minutes
    
    escrow_result = escrow_time.create_time_escrow(
        investor_wallet.seed,
        loan_amount_drops,
        farmer_wallet.address,
        finish_seconds,
        cancel_seconds
    )
    
    if "Submit failed" in str(escrow_result):
        print(f"   ❌ Escrow creation failed: {escrow_result}")
        return
    else:
        print(f"   ✅ Escrow created successfully!")
        print(f"   Sequence: {escrow_result.get('Sequence', 'N/A')}")
        escrow_sequence = escrow_result.get('Sequence', 0)
    
    # Check escrows
    print("4. Checking active escrows...")
    try:
        escrows = escrow_time.get_escrows(investor_wallet.address)
        if escrows.get('account_objects'):
            print(f"   Found {len(escrows['account_objects'])} escrow(s)")
            for escrow in escrows['account_objects']:
                print(f"   - Destination: {escrow.get('Destination', 'N/A')}")
                print(f"   - Amount: {int(escrow.get('Amount', 0)) / 1000000} XRP")
        else:
            print("   No active escrows found")
    except Exception as e:
        print(f"   Error checking escrows: {e}")
    
    # Test finishing escrow (farmer claims)
    print("5. Testing escrow finish (farmer claims funds)...")
    finish_result = escrow_time.finish_time_escrow(
        farmer_wallet.seed,
        investor_wallet.address,
        escrow_sequence
    )
    
    if "Submit failed" in str(finish_result):
        print(f"   ❌ Escrow finish failed: {finish_result}")
        # Try canceling instead
        print("6. Testing escrow cancel (investor reclaims)...")
        cancel_result = escrow_time.cancel_time_escrow(
            investor_wallet.seed,
            investor_wallet.address,
            escrow_sequence
        )
        if "Submit failed" in str(cancel_result):
            print(f"   ❌ Escrow cancel also failed: {cancel_result}")
        else:
            print(f"   ✅ Escrow cancelled successfully!")
    else:
        print(f"   ✅ Escrow finished successfully!")
    
    return investor_wallet, farmer_wallet

def test_conditional_escrow():
    """Test conditional escrow creation and operations"""
    print("\n=== TESTING CONDITIONAL ESCROW ===")
    
    # Create and fund wallets
    print("1. Creating investor and farmer wallets...")
    investor_wallet = wallet.get_account('')
    farmer_wallet = wallet.get_account('')
    
    print(f"   Investor: {investor_wallet.address}")
    print(f"   Farmer: {farmer_wallet.address}")
    
    # Generate condition and fulfillment
    print("2. Generating cryptographic condition...")
    condition, fulfillment = escrow_conditional.generate_condition()
    print(f"   Condition: {condition[:20]}...")
    print(f"   Fulfillment: {fulfillment[:20]}...")
    
    # Create conditional escrow
    print("3. Creating conditional escrow...")
    loan_amount = 3  # XRP
    loan_amount_drops = str(int(loan_amount * 1000000))
    cancel_seconds = 300  # 5 minutes
    
    escrow_result = escrow_conditional.create_conditional_escrow(
        investor_wallet.seed,
        loan_amount_drops,
        farmer_wallet.address,
        cancel_seconds,
        condition
    )
    
    if "Submit failed" in str(escrow_result):
        print(f"   ❌ Conditional escrow creation failed: {escrow_result}")
        return
    else:
        print(f"   ✅ Conditional escrow created successfully!")
        escrow_sequence = escrow_result.get('Sequence', 0)
        print(f"   Sequence: {escrow_sequence}")
    
    # Test finishing conditional escrow
    print("4. Testing conditional escrow finish...")
    finish_result = escrow_conditional.finish_conditional_escrow(
        farmer_wallet.seed,
        investor_wallet.address,
        escrow_sequence,
        condition,
        fulfillment
    )
    
    if "Submit failed" in str(finish_result):
        print(f"   ❌ Conditional escrow finish failed: {finish_result}")
    else:
        print(f"   ✅ Conditional escrow finished successfully!")
    
    return investor_wallet, farmer_wallet

def main():
    """Run all escrow tests"""
    print("🧪 ESCROW FUNCTIONALITY TESTS")
    print("=" * 50)
    
    try:
        # Test time-based escrow
        investor1, farmer1 = test_time_escrow()
        
        # Test conditional escrow
        investor2, farmer2 = test_conditional_escrow()
        
        print("\n=== TEST SUMMARY ===")
        print("✅ All escrow tests completed!")
        print("\nCreated wallets for testing:")
        if investor1:
            print(f"Time escrow - Investor: {investor1.address}")
            print(f"Time escrow - Farmer: {farmer1.address}")
        if investor2:
            print(f"Conditional escrow - Investor: {investor2.address}")
            print(f"Conditional escrow - Farmer: {farmer2.address}")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
