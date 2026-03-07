import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { proxyFactoryAbi } from "../../src/abis";
import { 
    CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS,
    NEG_RISK_ADAPTER_ADDRESS,
    PROXY_WALLET_FACTORY_ADDRESS,
    USDCE_DIGITS,
    USDC_ADDRESS
} from "../../src/constants";
import { encodeSplit } from "../../src/encode";


dotenvConfig({ path: resolve(__dirname, "../../.env") });


async function main() {
    console.log(`Starting...`);
    
    const provider = new ethers.providers.JsonRpcProvider(`${process.env.RPC_URL}`);
    const pk = new ethers.Wallet(`${process.env.PK}`);
    const wallet = pk.connect(provider);
    console.log(`Address: ${wallet.address}`)

    // Proxy factory
    const factory = new ethers.Contract(PROXY_WALLET_FACTORY_ADDRESS, proxyFactoryAbi, wallet);


    // =============== Replace the values below with your values ==========================
    const splitAmount = "1"; // replace with your split amount
    const conditionId = ""; // Replace with the market conditionId
    const negRisk = false; // Replace with the neg risk status of the market

    // Split
    const data = encodeSplit(USDC_ADDRESS, conditionId, ethers.utils.parseUnits(splitAmount, USDCE_DIGITS));
    const to = negRisk ? NEG_RISK_ADAPTER_ADDRESS: CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS;

    const proxyTxn = {
        to: to,
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