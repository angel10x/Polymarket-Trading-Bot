import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { safeAbi } from "../../src/abis";
import { CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS } from "../../src/constants";
import { encodeErc1155Approve } from "../../src/encode";
import { signAndExecuteSafeTransaction } from "../../src/safe-helpers";
import { OperationType, SafeTransaction } from "../../src/types";


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
    const spender = ""; // Replace with your destination address

    // Approves a spender for an ERC1155 token on the Safe
    const safeTxn: SafeTransaction = {
        to: CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS,
        operation: OperationType.Call,
        data: encodeErc1155Approve(spender, true),
        value: "0",
    };

    const txn = await signAndExecuteSafeTransaction(wallet, safe, safeTxn, {gasPrice: 200000000000});
    
    console.log(`Txn hash: ${txn.hash}`);
    await txn.wait();

    console.log(`Done!`)
}

main();
