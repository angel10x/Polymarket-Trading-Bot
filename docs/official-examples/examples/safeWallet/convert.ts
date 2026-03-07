import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { safeAbi } from "../../src/abis";
import { NEG_RISK_ADAPTER_ADDRESS, USDCE_DIGITS } from "../../src/constants";
import { encodeConvert } from "../../src/encode";
import { getIndexSet } from "../../src/utils";
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

    // Replace with the questionIds of the NO positions to be converted
    const questionIDs: string[] = [];
    const indexSet = getIndexSet(questionIDs);
    const convertAmount = "1"; // Replace with your convert amount
    // Replace with the event Neg Risk Market Id
    const marketId = "";

    const data = encodeConvert(marketId, indexSet, ethers.utils.parseUnits(convertAmount, USDCE_DIGITS));
    const to = NEG_RISK_ADAPTER_ADDRESS;

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