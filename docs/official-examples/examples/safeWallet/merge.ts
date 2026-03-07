import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { safeAbi } from "../../src/abis";
import { CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS, NEG_RISK_ADAPTER_ADDRESS, USDCE_DIGITS, USDC_ADDRESS } from "../../src/constants";
import { encodeMerge } from "../../src/encode";
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

    const mergeAmount = "1"; // replace with your split amount
    const conditionId = "0xe64f063b9e2b02f8ac679ebacfb938088c1ddde2a953a1ebfd4a92b802910371"; // Replace with the market conditionId
    const negRisk = true; // Replace with the neg risk status of the market

    const data = encodeMerge(USDC_ADDRESS, conditionId, ethers.utils.parseUnits(mergeAmount, USDCE_DIGITS));
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