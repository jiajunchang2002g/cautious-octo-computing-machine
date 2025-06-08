import json
from mod1 import get_account, get_account_info, send_xrp
from mod8 import create_time_escrow, finish_time_escrow, get_escrows, cancel_time_escrow, get_transaction

def print_json(data):
    print(json.dumps(data, indent=4))

def main():
    while True:
        print("\n--- XRP CLI Menu ---")
        print("1. Create new account (get_account)")
        print("2. Get account info")
        print("3. Send XRP")
        print("4. Create Time-based Escrow")
        print("5. Cancel Time-based Escrow")
        print("6. Finish Time-based Escrow")
        print("7. Get Escrows")
        print("8. Get Transaction")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            seed = input("Enter existing seed (leave blank to create new): ").strip()
            wallet = get_account(seed) if seed else get_account(None)
            print("Address:", wallet.classic_address)
            print("Seed:", wallet.seed)

        elif choice == "2":
            acct = input("Enter account address: ").strip()
            info = get_account_info(acct)
            print_json(info)

        elif choice == "3":
            seed = input("Sender seed: ").strip()
            dest = input("Destination address: ").strip()
            amt = input("Amount (in XRP drops): ").strip()
            response = send_xrp(seed, amt, dest)
            print_json(response.result)

        elif choice == "4":
            seed = input("Sender seed: ").strip()
            amt = input("Amount (in XRP drops): ").strip()
            dest = input("Destination address: ").strip()
            finish = input("Escrow Finish (unix seconds from now): ").strip()
            cancel = input("Escrow Cancel (unix seconds from now): ").strip()
            result = create_time_escrow(seed, amt, dest, finish, cancel)
            print_json(result)

        elif choice == "5":
            seed = input("Seed of escrow creator: ").strip()
            owner = input("Escrow owner address: ").strip()
            seq = input("Escrow sequence number: ").strip()
            result = cancel_time_escrow(seed, owner, seq)
            print_json(result)

        elif choice == "6":
            seed = input("Finisher's seed: ").strip()
            owner = input("Escrow owner address: ").strip()
            seq = input("Escrow sequence number: ").strip()
            result = finish_time_escrow(seed, owner, seq)
            print_json(result)

        elif choice == "7":
            acct = input("Account to check escrows for: ").strip()
            result = get_escrows(acct)
            print_json(result)

        elif choice == "8":
            acct = input("Account address: ").strip()
            tx_hash = input("Transaction hash: ").strip()
            result = get_transaction(acct, tx_hash)
            print_json(result)

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
