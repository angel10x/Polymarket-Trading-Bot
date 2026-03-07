import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { safeAbi } from "../../src/abis";
import { CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS, USDCE_DIGITS } from "../../src/constants";
import { encodeErc1155TransferFrom } from "../../src/encode";
import { signAndExecuteSafeTransaction } from "../../src/safe-helpers";


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
    const to = ""; // Replace with your destination address
    const tokenId = ""; // Replace with your tokenId
    const value = ethers.utils.parseUnits("1", USDCE_DIGITS); // Replace with your transfer value
    // Transfers an ERC1155 token out of the Safe to the destination address
    const data = encodeErc1155TransferFrom(safeAddress, to, tokenId, value);
    
    const token = CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS;
    const txn = await signAndExecuteSafeTransaction(wallet, safe, token, data, {gasPrice: 200000000000});
    
    console.log(`Txn hash: ${txn.hash}`);
    await txn.wait();

    console.log(`Done!`)
}

main();