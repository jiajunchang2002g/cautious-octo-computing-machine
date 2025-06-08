
# WeGro - Farmer Crowdfunding Platform on XRP Ledger

<150 chars summary: A decentralized crowdfunding platform for farmers using XRP Ledger with tokenized investments, escrow-based microloans, and transparent funding.

## 🎯 Problem Statement

Small-scale farmers worldwide face critical funding challenges:
- **Limited Access to Capital**: Traditional banks often reject agricultural loans due to perceived risks
- **High Transaction Costs**: Payment processors charge 3-5% fees, eating into already thin margins
- **Lack of Transparency**: Investors have no visibility into how funds are used or project progress
- **Geographic Barriers**: Rural farmers can't access global investment opportunities
- **Trust Issues**: No verifiable system for investors to track their contributions and returns

## 💡 Solution

WeGro leverages the XRP Ledger to create a transparent, low-cost, and decentralized crowdfunding ecosystem that connects farmers directly with global investors.

### Key Features:
1. **Tokenized Investments**: Each approved farm project mints custom IOU tokens representing investor stakes
2. **Escrow-Based Microloans**: Time-locked smart contracts ensure secure lending with automatic execution
3. **Direct XRP Funding**: Farmers receive XRP directly to their wallets with minimal fees (<$0.01)
4. **Transparent Tracking**: All transactions are recorded on the XRP Ledger for full audit trails
5. **Global Access**: Anyone with internet can participate as farmer or investor

## 🔧 Technical Implementation

### XRP Ledger Features Used:
- **IOU Tokens**: Custom currency codes for project-specific tokens (3-character identifiers)
- **Trust Lines**: Enables investors to receive and hold project tokens
- **Escrow Functionality**: Time-based conditional payments for microloans
- **Payment Channels**: Direct XRP transfers between investors and farmers
- **Account Settings**: Configure accounts for token issuance with default ripple flags

### SDKs and Technologies:
- **xrpl-py SDK v4.1.0**: Primary interface for XRP Ledger interactions
- **cryptoconditions**: For escrow condition generation and fulfillment
- **Python 3.11+**: Core application logic and CLI interface
- **JSON Storage**: Local data persistence for campaign and investment tracking

### Unique XRP Ledger Advantages:
1. **Sub-second Settlement**: Instant XRP transfers enable real-time funding
2. **Minimal Fees**: ~$0.0001 per transaction vs. 3-5% traditional payment fees
3. **Built-in DEX**: Native token exchange capabilities for future trading
4. **Escrow Primitives**: No smart contract complexity, native escrow support
5. **Global Accessibility**: No geographic restrictions or banking requirements

## 🏗️ Architecture

```
WeGro Platform Architecture:

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Farmers     │    │   Investors     │    │     Admin       │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                WeGro CLI Interface                              │
├─────────────────────────────────────────────────────────────────┤
│              CrowdfundingPlatform Core Logic                    │
├─────────────────────────────────────────────────────────────────┤
│    Wallet Utils  │  Token Utils   │  Escrow Utils  │  Storage   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    XRP Ledger (Testnet)                        │
│  • Wallet Generation  • IOU Tokens  • Escrow Contracts         │
│  • XRP Payments      • Trust Lines  • Account Configuration    │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 User Flow

### For Farmers:
1. **Create Campaign**: Farmer inputs project details and funding goals
2. **Receive Wallet**: System generates XRPL wallet and provides seed phrase
3. **Wait for Approval**: Admin reviews and approves legitimate campaigns
4. **Token Minting**: System creates project-specific IOU tokens
5. **Receive Funding**: Investors send XRP directly to farmer's wallet

### For Investors:
1. **Browse Campaigns**: View all approved farming projects
2. **Select Investment**: Choose campaign and investment amount
3. **Send XRP**: Transfer XRP to farmer's wallet address
4. **Receive Tokens**: Automatically receive project tokens (1:1 ratio)
5. **Track Investment**: Monitor project progress and token balance

### For Microloans:
1. **Create Escrow**: Investor locks XRP for specific farmer and timeframe
2. **Farmer Claims**: After time period, farmer can claim escrowed funds
3. **Auto-Cancellation**: If unclaimed, investor can reclaim after grace period

## 📊 XRPL Transaction Flow

### Campaign Investment Process:
```
1. Investor → Farmer: XRP Payment
   Transaction Type: Payment
   Amount: Investment XRP
   Fee: ~0.00001 XRP

2. Investor → XRPL: Trust Line Creation
   Transaction Type: TrustSet
   Currency: Project Token (e.g., "MAI" for Maize)
   Limit: Investment Amount × 10

3. Farmer → Investor: Token Distribution
   Transaction Type: Payment
   Currency: Project Token
   Amount: 1:1 ratio with XRP investment
```

### Microloan Escrow Process:
```
1. Investor → XRPL: Escrow Creation
   Transaction Type: EscrowCreate
   Amount: Loan XRP
   Destination: Farmer Address
   FinishAfter: Loan Duration
   CancelAfter: Loan Duration + Grace Period

2. Farmer → XRPL: Escrow Claim
   Transaction Type: EscrowFinish
   Owner: Investor Address
   Sequence: Escrow Sequence Number
```

## 📱 Demo Video

[🎥 Watch Full Demo Video](https://www.loom.com/share/41fc49e649784751a541563ed693ebb8?sid=f6439042-12df-48ea-b7d7-f94327d0a8e3)

*This video demonstrates:*
- Complete farmer campaign creation process
- Admin approval and token minting
- Investor funding and token receipt
- Microloan creation and claiming
- Live XRPL testnet transactions

## 🖼️ Screenshots

### Campaign Management Interface
![Campaign Creation](https://your-screenshot-url/campaign-creation.png)
*Farmers can easily create campaigns with project details and funding goals*

### Investment Dashboard
![Investment Process](https://your-screenshot-url/investment-process.png)
*Investors browse approved campaigns and fund projects directly*

### Microloan System
![Microloan Interface](https://your-screenshot-url/microloan-system.png)
*Escrow-based microloans with automatic time-based execution*

### XRPL Transaction Confirmation
![XRPL Transactions](https://your-screenshot-url/xrpl-transactions.png)
*Real-time confirmation of XRP transfers and token distributions*

## 🔗 Live Transactions

### Testnet Block Explorer Links:
- **Campaign Creation**: [View Transaction](https://testnet.xrpl.org/transactions/YOUR_CAMPAIGN_TX_HASH)
- **Token Minting**: [View Transaction](https://testnet.xrpl.org/transactions/YOUR_TOKEN_TX_HASH)
- **Investment Payment**: [View Transaction](https://testnet.xrpl.org/transactions/YOUR_PAYMENT_TX_HASH)
- **Escrow Creation**: [View Transaction](https://testnet.xrpl.org/transactions/YOUR_ESCROW_TX_HASH)

### Test Wallets:
- **Sample Farmer**: `rXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
- **Sample Investor**: `rYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY`

## 🎨 Presentation

[📊 View Canva Presentation](https://www.canva.com/design/your-presentation-link)

*Includes slides on:*
- Team Introduction
- Problem Statement
- Solution Overview
- Technical Architecture
- XRP Ledger Integration
- Demo and Results

## 🛠️ Installation & Setup

### Prerequisites:
- Python 3.11+
- Git

### Quick Start:
```bash
# Clone the repository
git clone https://github.com/your-username/wegro-crowdfunding

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### Usage:
1. **Create Campaign**: Option 1 - Input farmer details and project info
2. **Approve Campaign**: Option 3 - Admin approves and mints tokens
3. **Invest in Campaign**: Option 4 - Send XRP and receive project tokens
4. **Create Microloan**: Option 5 - Set up escrow-based lending
5. **Check Balances**: Options 9-10 - View XRP and token balances

## 💰 Economic Model

### For Farmers:
- **No Upfront Costs**: Platform generates free XRPL wallets
- **Minimal Fees**: Only standard XRPL transaction fees (~$0.0001)
- **Direct Funding**: Receive XRP immediately upon investment
- **Token Rewards**: Keep percentage of project tokens for future value

### For Investors:
- **Low Barrier**: Minimum investment as low as 1 XRP
- **Transparent Returns**: Project tokens represent verifiable stakes
- **Global Access**: Invest in farms worldwide without intermediaries
- **Liquidity Options**: Trade tokens on XRPL DEX (future feature)

## 🔒 Security Features

- **Seed Phrase Protection**: Users maintain custody of their wallet seeds
- **Escrow Safety**: Time-locked contracts prevent fraud in microloans
- **Admin Controls**: Campaign approval prevents spam and scams
- **Transaction Transparency**: All operations recorded on public ledger
- **No Custodial Risk**: Platform never holds user funds

## 🌍 Impact & Scalability

### Current Scope:
- **Proof of Concept**: Fully functional CLI application
- **Testnet Deployment**: All transactions on XRPL testnet
- **Core Features**: Campaign management, investments, microloans

### Future Roadmap:
- **Web Interface**: User-friendly web application
- **Mobile App**: React Native app for farmers and investors
- **Advanced Features**: Yield tracking, insurance products, governance tokens
- **Mainnet Launch**: Production deployment with real XRP
- **Global Expansion**: Support for multiple languages and regions

## 📈 Business Model

1. **Transaction Fees**: Small percentage on campaign funding (1-2%)
2. **Premium Features**: Advanced analytics and marketing tools for farmers
3. **Partnership Revenue**: Integration fees from agricultural cooperatives
4. **Token Economics**: Platform governance tokens for stakeholder voting

## 🤝 Team

- **Lead Developer**: Blockchain integration and XRPL implementation
- **Agricultural Advisor**: Farmer needs assessment and market validation
- **UX Designer**: User interface and experience optimization
- **Business Development**: Partnership and growth strategies

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🔗 Links

- **GitHub Repository**: [https://github.com/your-username/wegro-crowdfunding](https://github.com/your-username/wegro-crowdfunding)
- **Canva Presentation**: [https://www.canva.com/design/your-presentation-link](https://www.canva.com/design/your-presentation-link)
- **Demo Video**: [https://www.loom.com/share/your-demo-video-link](https://www.loom.com/share/your-demo-video-link)
- **XRPL Testnet Explorer**: [https://testnet.xrpl.org/](https://testnet.xrpl.org/)

---

*Built with ❤️ for farmers worldwide using the power of XRP Ledger*
