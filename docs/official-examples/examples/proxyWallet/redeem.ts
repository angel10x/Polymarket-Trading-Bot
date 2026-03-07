import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { proxyFactoryAbi } from "../../src/abis";
import { 
    CONDITIONAL_TOKENS_FRAMEWORK_ADDRESS,
    NEG_RISK_ADAPTER_ADDRESS,
    PROXY_WALLET_FACTORY_ADDRESS,
    USDC_ADDRESS
} from "../../src/constants";
import { encodeRedeem, encodeRedeemNegRisk } from "../../src/encode";


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
    const conditionId = ""; // Replace with the market conditionId
    const negRisk = true; // Replace with the neg risk status of the market
    
    // amounts of conditional tokens to redeem. Only used for neg risk redeemds
    // should always have length 2, with the first element being the amount of yes tokens to redeem and the
    // second element being the amount of no tokens to redeem
    // Only necessary for redeeming neg risk tokens
    const redeemAmounts = ["1", "1"]; 
    
    // Redeem
    const data = negRisk ? encodeRedeemNegRisk(conditionId, redeemAmounts) : encodeRedeem(USDC_ADDRESS, conditionId);
        
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