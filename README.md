Be built on the XRP Ledger

Be open source (and remain available as open source)

Include a short summary (<150 chars)

Core Features
1. Campaign Management

    Create Campaign: Farmers can create crowdfunding campaigns with project details, funding goals, and automatically generated XRPL wallets
    List Campaigns: View all campaigns with status, funding goals, and project information
    Approve Campaign: Admin function to approve campaigns and mint project-specific IOU tokens

2. XRPL Integration

    Wallet Generation: Automatic XRPL wallet creation for farmers using testnet faucet
    Token Minting: Creates custom IOU tokens (3-character currency codes) for each approved project
    Account Configuration: Sets up farmer accounts for token issuance with default ripple flag

3. Investment System

    XRP Investment: Investors can send XRP directly to farmer wallets
    Token Distribution: Investors receive project tokens (1:1 ratio with XRP investment)
    Trust Lines: Automatic trust line creation for investors to receive tokens
    Investment Tracking: Records all investments with timestamps and amounts

4. Wallet Management

    Balance Checking: Check both XRP and token balances for any wallet
    Seed Management: Secure wallet seed generation and storage
    New Investor Wallets: Automatic wallet creation for new investors

5. Data Persistence

    JSON Storage: Campaign and investment data stored in 

    Auto-initialization: Storage file created automatically on first run

6. CLI Interface

    Interactive command-line interface with 6 main options
    User-friendly prompts and confirmations
    Error handling for invalid inputs

Technical Implementation

    Built on XRPL testnet using xrpl-py SDK
    Modular architecture with separate modules for XRPL operations 
    Campaign lifecycle: Create → Approve → Invest
    Real XRPL transactions for all operations (XRP transfers, token issuance, trust lines

Include a full description (the problems it solves, how the XRP Ledger was used to achieve it)

Include a technical description (what SDKs were used, and what features of the XRP Ledger made this uniquely possible)

Include a link to the Canva slides used in the presentation (including a slide on your team, problem, solution etc). You must use Canva for your presentation (yes, this is a requirement).

Have a custom (not boilerplate) app and transactions on the XRP Ledger (and committed to your GitHub repo). All of this must be fully-functioning, as evidenced in a demo video on your README (see point 8 below).

Include a clear README on your GitHub repo explaining how your project works. This README must include:

A demo video

Screenshots of your UI

Description of how your interaction with the XRP Ledger works

A video with audio (e.g. a Loom video like this) explaining how your project works, how the GitHub repo is structured, a demo of everything working etc. This is vital, so that the judges can review your project properly. Make sure you explain clearly how you satisfied point 7 above. This is a great example of a project README: https://github.com/mahir-pa/poap. Bonus points for if your video is well-edited!

Block explorer link for transactions from your dApp on the XRP Ledger testnet


