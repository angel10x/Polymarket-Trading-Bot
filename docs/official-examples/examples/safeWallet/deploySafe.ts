import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";
import { Zero, AddressZero } from "@ethersproject/constants";
import { splitSignature } from "@ethersproject/bytes";

import { safeFactoryAbi } from "../../src/abis";
import { SAFE_FACTORY_ADDRESS } from "../../src/constants";
import { createSafeCreateSignature } from "../../src/safe-helpers";

dotenvConfig({ path: resolve(__dirname, "../../.env") });

async function main() {
    console.log(`Starting...`);
    
    const provider = new ethers.providers.JsonRpcProvider(`${process.env.RPC_URL}`);
    const pk = new ethers.Wallet(`${process.env.PK}`);
    const wallet = pk.connect(provider);
    const chainId = await wallet.getChainId();

    console.log(`Address: ${wallet.address}`)

    const factory = new ethers.Contract(SAFE_FACTORY_ADDRESS, safeFactoryAbi, wallet);
    
    // Create the safe create signature
    const sig = await createSafeCreateSignature(wallet, chainId);

    // Execute
    const txn = await factory.createProxy(
        AddressZero,
        Zero,
        AddressZero,
        splitSignature(sig),
        {gasPrice: 100000000000},
    );
    console.log(`txn hash: ${txn.hash}`);
    await txn.wait();

    console.log(`Done!`);
}

main();


