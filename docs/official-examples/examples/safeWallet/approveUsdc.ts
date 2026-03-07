import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { safeAbi } from "../../src/abis";
import { USDC_ADDRESS } from "../../src/constants";
import { encodeErc20Approve } from "../../src/encode";
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

    const spender = ""; // Replace with your destination address
    const approvalAmount = ethers.constants.MaxUint256;
    // Approves a spender for an ERC20 token on the Safe
    const data = encodeErc20Approve(spender, approvalAmount);
    
    const safeTxn: SafeTransaction = {
        to: USDC_ADDRESS,
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