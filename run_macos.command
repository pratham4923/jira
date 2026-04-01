#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
chmod +x "$DIR/run_macos.sh"
exec "$DIR/run_macos.sh"
