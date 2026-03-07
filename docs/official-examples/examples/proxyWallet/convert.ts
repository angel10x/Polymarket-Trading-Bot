import { ethers } from "ethers";
import { config as dotenvConfig } from "dotenv";
import { resolve } from "path";

import { proxyFactoryAbi } from "../../src/abis";
import { 
    NEG_RISK_ADAPTER_ADDRESS,
    PROXY_WALLET_FACTORY_ADDRESS,
    USDCE_DIGITS
} from "../../src/constants";
import { encodeConvert } from "../../src/encode";
import { getIndexSet } from "../../src/utils";


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
    // Replace with the questionIds of the NO positions to be converted
    const questionIDs: string[] = [""];
    const indexSet = getIndexSet(questionIDs);
    const convertAmount = "1"; // replace with your merge amount
    // Replace with the event Neg Risk Market Id
    const marketId = "";

    const data = encodeConvert(marketId, indexSet, ethers.utils.parseUnits(convertAmount, USDCE_DIGITS));
    const to = NEG_RISK_ADAPTER_ADDRESS;

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
