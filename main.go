package main

import (
	"context"
	"log"
	"os"

	"github.com/enmand/alice/cmd"
)

func main() {
	ctx := context.Background()

	if err := cmd.Root.Run(ctx, os.Args); err != nil {
		log.Fatalf("Error executing command: %v", err)
	}
}
