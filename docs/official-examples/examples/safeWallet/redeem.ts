import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { safeAbi } from "../../src/abis";
import { CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS, NEG_RISK_ADAPTER_ADDRESS, USDCE_DIGITS, USDC_ADDRESS } from "../../src/constants";
import { encodeRedeem, encodeRedeemNegRisk } from "../../src/encode";
import { signAndExecuteSafeTransaction } from "../../src/safe-helpers";
import { SafeTransaction, OperationType } from "../../src/types";


dotenvConfig({ path: resolve(__dirname, "../../.env") });


async function main() {
    console.log(`Starting...`);
    
    const provider = new ethers.providers.JsonRpcProvider(`${process.env.RPC_URL}`);
    const pk = new ethers.Wallet(`${process.env.PK}`);
    const wallet = pk.connect(provider);

    console.log(`Address: ${wallet.address}`)

    // =============== Replace the values below with your values ==========================
    // Safe
    const safeAddress = ""; // Replace with your safe address
    const safe = new ethers.Contract(safeAddress, safeAbi, wallet);

    const conditionId = ""; // Replace with the market conditionId
    const negRisk = true; // Replace with the neg risk status of the market

    // amounts of conditional tokens to redeem. Only used for neg risk redeems
    // should always have length 2, with the first element being the amount of yes tokens to redeem and the
    // second element being the amount of no tokens to redeem
    // Only necessary for redeeming neg risk tokens
    const redeemAmounts = ["1", "1"];
    const data = negRisk ? encodeRedeemNegRisk(conditionId, redeemAmounts) : encodeRedeem(USDC_ADDRESS, conditionId);
    const to = negRisk ? NEG_RISK_ADAPTER_ADDRESS: CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS;


    const safeTxn: SafeTransaction = {
        to: to,
        data: data,
        operation: OperationType.Call,
        value: "0",
    };

    const txn = await signAndExecuteSafeTransaction(wallet, safe, safeTxn, {gasPrice: 200000000000});
    
    console.log(`Txn hash: ${txn.hash}`);
    await txn.wait();

    console.log(`Done!`)
}

main();