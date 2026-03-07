import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { safeAbi } from "../../src/abis";
import { CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS, USDC_ADDRESS } from "../../src/constants";
import { encodeErc1155Approve, encodeErc20Approve } from "../../src/encode";
import { aggregateTransaction, signAndExecuteSafeTransaction } from "../../src/safe-helpers";
import { OperationType, SafeTransaction } from "../../src/types";


dotenvConfig({ path: resolve(__dirname, "../../.env") });

// This example does all approvals necessary for trading
// Approves:
// USDC on the CTF Contract
// USDC on the Neg Risk Adapter
// USDC on the CTF Exchange Contract
// USDC on the Neg Risk Exchange Contract

// CTF Outcome Tokens on the CTF Exchange Contract
// CTF Outcome Tokens on the Neg Risk Exchange Contract
// CTF Outcome Tokens on the Neg Risk Adapter
async function main() {
    console.log(`Starting...`);
    
    const provider = new ethers.providers.JsonRpcProvider(`${process.env.RPC_URL}`);
    const pk = new ethers.Wallet(`${process.env.PK}`);
    const wallet = pk.connect(provider);

    console.log(`Address: ${wallet.address}`)

    // Safe
    const safeAddress = ""; // Replace with your safe address
    const safe = new ethers.Contract(safeAddress, safeAbi, wallet);
    
    const usdcSpenders = [
        "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045", // Conditional Tokens Framework
        "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", // Neg Risk Adapter
        "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", // CTF Exchange
        "0xC5d563A36AE78145C45a50134d48A1215220f80a", // Neg Risk CTF Exchange
    ];

    const outcomeTokenSpenders = [
        "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", // CTF Exchange
        "0xC5d563A36AE78145C45a50134d48A1215220f80a", // Neg Risk Exchange
        "0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", // Neg Risk Adapter
    ];

    const safeTxns: SafeTransaction[] = [];
    
    for(const spender of usdcSpenders) {
        safeTxns.push(
            {
                to: USDC_ADDRESS,
                data: encodeErc20Approve(spender, ethers.constants.MaxUint256),
                operation: OperationType.Call,
                value: "0",
            }
        );
    }

    for(const spender of outcomeTokenSpenders) {
        safeTxns.push(
            {
                to: CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS,
                data: encodeErc1155Approve(spender, true),
                operation: OperationType.Call,
                value: "0",
            }
        );
    }

    const safeTxn = aggregateTransaction(safeTxns);
    const txn = await signAndExecuteSafeTransaction(wallet, safe, safeTxn, {gasPrice: 200000000000});
    
    console.log(`Txn hash: ${txn.hash}`);
    await txn.wait();

    console.log(`Done!`)
}

main();
