package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"os/exec"
)

const DATENBANK_PATH = "/datenbank/datenbank.db"
const EMPTY_DATENBANK_PATH = "/app/datenbank_empty.db"

func main() {
	fmt.Println("[Runner][Info]   Preparing python server runtime...")

	fmt.Println("[Runner][Info]   Checking datenbank in volume...")

	info, err := os.Stat(DATENBANK_PATH)

	isDbError := false

	if err != nil || info.IsDir() {
		func() {
			fmt.Println("[Runner][Info]   /datenbank/datenbank.db not exists, copy an empty one")
			dstDbFile, err := os.OpenFile(DATENBANK_PATH, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, os.ModePerm)

			if err != nil {
				fmt.Println("[Runner][Error]   Cannot write datenbank file, aborting...")
				isDbError = true
				return
			}
			defer dstDbFile.Close()

			srcDbFile, err := os.OpenFile(EMPTY_DATENBANK_PATH, os.O_RDONLY, os.FileMode(0444))

			if err != nil {
				fmt.Println("[Runner][Error]   Cannot open source empty datenbank file, aborting...")
				isDbError = true
				return
			}
			defer srcDbFile.Close()

			if _, err := io.Copy(dstDbFile, srcDbFile); err != nil {
				fmt.Println("[Runner][Error]   Cannot copy source empty datenbank file, aborting...")
				isDbError = true
				return
			}
		}()
	}

	if isDbError {
		fmt.Println("[Runner][Error]   Initialized datenbank.db failed")
		os.Exit(-1)
	}

	fmt.Println("[Runner][Info]   datenbank.db is initialized")

	cmd := exec.Command("./server")
	cmd.Dir = "/app"

	procStdoutPipe, err := cmd.StdoutPipe()
	cmd.Stderr = cmd.Stdout

	if err != nil {
		fmt.Println("[Runner][Error]   Cannot create standard output pipe, aborting...")
		fmt.Println("[Runner][Error]   Start gunicorn server executable failed")
		os.Exit(-1)
	}

	if err := cmd.Start(); err != nil {
		fmt.Println("[Runner][Error]   Cannot start gunicorn server executable, aborting...")
		fmt.Println("[Runner][Error]   Start gunicorn server executable failed")
		os.Exit(-1)
	}

	terminateSignal := make(chan bool)

	go func() {
		fmt.Println("[Runner][Info]   Starting gunicorn server...")
		cmd.Wait()
		terminateSignal <- true
	}()

	reader := bufio.NewReader(procStdoutPipe)
	go func() {
		for {
			line, err := reader.ReadString('\n')

			if err != nil {
				break
			}

			fmt.Printf("[Gunicorn][Info]  %s\n", line)
		}
	}()

	fmt.Println("[Runner][Info]   Gunicorn server start successfully")
	fmt.Println("[Runner][Info]   Waiting for Gunicorn terminate, processing normal requests...")

	<-terminateSignal
}
