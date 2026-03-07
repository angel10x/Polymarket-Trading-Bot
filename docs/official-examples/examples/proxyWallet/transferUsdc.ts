import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { proxyFactoryAbi } from "../../src/abis";
import { PROXY_WALLET_FACTORY_ADDRESS, USDCE_DIGITS, USDC_ADDRESS } from "../../src/constants";
import { encodeErc20Transfer } from "../../src/encode";


dotenvConfig({ path: resolve(__dirname, "../../.env") });


async function main() {
    console.log(`Starting...`);
    
    const provider = new ethers.providers.JsonRpcProvider(`${process.env.RPC_URL}`);
    const pk = new ethers.Wallet(`${process.env.PK}`);
    const wallet = pk.connect(provider);

    // Proxy factory
    const factory = new ethers.Contract(PROXY_WALLET_FACTORY_ADDRESS, proxyFactoryAbi, wallet);

    console.log(`Address: ${wallet.address}`)

    // =============== Replace the values below with your values ==========================
    const to = ""; // Replace with your destination address
    const value = ethers.utils.parseUnits("1", USDCE_DIGITS); // Replace with your transfer value
    
    // Transfers an ERC20 token out of the proxy wallet to the destination address
    const data = encodeErc20Transfer(to, value);
    
    const proxyTxn = {
        to: USDC_ADDRESS,
        typeCode: "1",
        data: data,
        value: "0",
    };

    const txn = await factory.proxy([proxyTxn], { gasPrice: 100000000000 });
    
    console.log(`Txn hash: ${txn.hash}`);
    await txn.wait();

    console.log(`Done!`)
}

main();