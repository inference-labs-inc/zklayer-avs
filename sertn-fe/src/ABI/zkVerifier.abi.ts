export const zkVerifier = [
  {
    type: "function",
    name: "verifyProof",
    inputs: [
      { internalType: "bytes", name: "proof", type: "bytes" },
      { internalType: "uint256[]", name: "instances", type: "uint256[]" },
    ],
    outputs: [{ internalType: "bool", name: "", type: "bool" }],
    stateMutability: "nonpayable",
  },
];
