export enum CallType {
    Invalid = "0",
    Call = "1",
    DelegateCall = "2",
}
  
export interface ProxyTransaction {
    to: string;
    typeCode: CallType;
    data: string;
    value: string;
}

// Safe Transactions
export enum OperationType {
    Call, // 0
    DelegateCall, // 1
}  

export interface SafeTransaction {
    to: string;
    operation: OperationType
    data: string;
    value: string;
}