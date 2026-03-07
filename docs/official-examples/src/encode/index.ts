import { BigNumber, ethers, BigNumberish } from "ethers";
import { Interface } from "ethers/lib/utils";
import { erc20Abi, erc1155Abi, ctfAbi, negRiskAdapterAbi } from "../abis"


const ERC20_INTERFACE = new Interface(erc20Abi);
const ERC1155_INTERFACE = new Interface(erc1155Abi);
const CTF_INTERFACE = new Interface(ctfAbi);
const NEG_RISK_INTERFACE = new Interface(negRiskAdapterAbi);


export const encodeErc20Transfer = (to: string, value: BigNumber): string => {
    return ERC20_INTERFACE.encodeFunctionData(
        "transfer(address,uint256)",
        [to, value]
    );
}

export const encodeErc1155TransferFrom = (from: string, to: string, id: string, value: BigNumber): string => {
    return ERC1155_INTERFACE.encodeFunctionData(
        "safeTransferFrom(address,address,uint256,uint256,bytes)",
        [from, to, id, value, ethers.constants.HashZero]
    );
}

export const encodeErc20Approve = (spender: string, approvalAmount: BigNumber): string => {
    return ERC20_INTERFACE.encodeFunctionData(
        "approve(address,uint256)",
        [spender, approvalAmount]
    );
}

export const encodeErc1155Approve = (spender: string, approval: boolean): string => {
    return ERC1155_INTERFACE.encodeFunctionData(
        "setApprovalForAll(address,bool)",
        [spender, approval],
    );
}

export const encodeSplit = (collateralToken: string, conditionId: string, amount: BigNumber) : string => {
    return CTF_INTERFACE.encodeFunctionData(
        "splitPosition(address,bytes32,bytes32,uint256[],uint256)",
        [collateralToken, ethers.constants.HashZero, conditionId, [1, 2], amount],
    );
}

export const encodeMerge = (collateralToken: string, conditionId: string, amount: BigNumber) : string => {
    return CTF_INTERFACE.encodeFunctionData(
        "mergePositions(address,bytes32,bytes32,uint256[],uint256)",
        [collateralToken, ethers.constants.HashZero, conditionId, [1, 2], amount],
    );
}

export const encodeRedeem = (collateralToken: string, conditionId: string) : string => {
    return CTF_INTERFACE.encodeFunctionData(
        "redeemPositions(address,bytes32,bytes32,uint256[])",
        [collateralToken, ethers.constants.HashZero, conditionId, [1, 2]],
    );
}

export const encodeRedeemNegRisk = (conditionId: string, amounts: string[]): string => {
    return NEG_RISK_INTERFACE.encodeFunctionData(
        "redeemPositions(bytes32,uint256[])",
        [conditionId, amounts],
    );
}

export const encodeConvert = (marketId: string, indexSet: BigNumberish, amount: BigNumberish) : string => {
    return NEG_RISK_INTERFACE.encodeFunctionData(
        "convertPositions(bytes32,uint256,uint256)",
        [marketId, indexSet, amount],
    ); 
}