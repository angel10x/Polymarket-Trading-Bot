import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { proxyFactoryAbi } from "../../src/abis";
import { 
    CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS,
    PROXY_WALLET_FACTORY_ADDRESS,
    USDC_ADDRESS
} from "../../src/constants";
import { encodeErc1155Approve, encodeErc20Approve } from "../../src/encode";
import { ProxyTransaction, CallType } from "../../src/types";


dotenvConfig({ path: resolve(__dirname, "../../.env") });

// This example does all approvals necessary for trading
// Approves:
// USDC on the CTF Contract
// USDC on the CTF Exchange Contract
// USDC on the Neg Risk Exchange Contract
// USDC on the Neg Risk Adapter contract
// CTF Outcome Tokens on the CTF Exchange Contract
// CTF Outcome Tokens on the Neg Risk Exchange Contract
async function main() {
    console.log(`Starting...`);
    
    const provider = new ethers.providers.JsonRpcProvider(`${process.env.RPC_URL}`);
    const pk = new ethers.Wallet(`${process.env.PK}`);
    const wallet = pk.connect(provider);

    console.log(`Address: ${wallet.address}`)

    // Proxy factory
    const factory = new ethers.Contract(PROXY_WALLET_FACTORY_ADDRESS, proxyFactoryAbi, wallet);

    const txns: ProxyTransaction[]  = [];
    const usdcSpenders = [
        "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045", // Conditional Tokens Framework
        "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", // CTF Exchange
        "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", // Neg Risk Adapter
        "0xC5d563A36AE78145C45a50134d48A1215220f80a", // Neg Risk CTF Exchange
    ];

    const outcomeTokenSpenders = [
        "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", // CTF Exchange
        "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", // Neg Risk Adapter
        "0xC5d563A36AE78145C45a50134d48A1215220f80a", // Neg Risk Exchange
    ];

    for(const spender of usdcSpenders) {
        // Approves a spender for an ERC20 token on the Proxy Wallet
        txns.push({
            to: USDC_ADDRESS,
            typeCode: CallType.Call,
            data: encodeErc20Approve(spender, ethers.constants.MaxUint256),
            value: "0",
        });
    }

    for(const spender of outcomeTokenSpenders) {
        // Approves a spender for an ERC1155 token on the Proxy Wallet
        txns.push({
            to: CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS,
            typeCode: CallType.Call,
            data: encodeErc1155Approve(spender, true),
            value: "0",
        });
    }

    const txn = await factory.proxy(txns, { gasPrice: 100000000000 });

    console.log(`Txn hash: ${txn.hash}`);
    await txn.wait();

    console.log(`Done!`)
}

main();