package tests

import (
	"bytes"
	"fmt"
	"log"
	"math/big"
	"os/exec"
	"time"
)

// Make sure to stop the anvil subprocess by calling anvilCmd.Process.Kill()
func StartAnvilChainAndDeployContracts() *exec.Cmd {
	fmt.Println("Starting anvil...")
	anvilCmd := exec.Command("anvil", "--fork-url", "https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161")
	err := anvilCmd.Start()
	if err != nil {
		log.Fatal(err.Error())
	}

	fmt.Println("Sleeping for 2 seconds to give time for anvil to start before we deploy contracts...")
	time.Sleep(2 * time.Second)

	fmt.Println("Deploying contracts...")
	cmd := exec.Command("forge", "script", "script/ZklayerDeployer.s.sol",
		"--rpc-url", "http://localhost:8545",
		"--private-key", "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
		"--broadcast",
	)
	cmd.Dir = "./contracts"
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err = cmd.Run()

	if err != nil {
		fmt.Println(stderr.String())
		log.Fatal(err.Error())
	}
	fmt.Println(stdout.String())

	return anvilCmd
}

func TestInputs() [5]*big.Int {
	inputs := [5]*big.Int{big.NewInt(0), big.NewInt(0), big.NewInt(0), big.NewInt(1), big.NewInt(0)}
	return inputs
}

func GoodOutput() *big.Int {
	return big.NewInt(1)
}

func BadOutput() *big.Int {
	return big.NewInt(0)
}

func OutputAndProof() (*big.Int, []byte) {
	proof := []byte{byte(0)}
	return GoodOutput(), proof
}
