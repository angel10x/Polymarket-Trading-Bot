
const getMarketIndex = (questionId: string): number => parseInt(questionId.slice(-2), 16);

export const getIndexSet = (questionIds: string[]) => {
    const indices = questionIds.map((id) => getMarketIndex(id));
    return [...new Set(indices)].reduce((acc, index) => acc + (1 << index), 0);
}
    

