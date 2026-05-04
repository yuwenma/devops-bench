#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/third_party/gke-mcp"
VERSION="${1:-main}"

if [ ! -d "$REPO_DIR" ]; then
  echo "Cloning gke-mcp (version: $VERSION)..."
  git clone https://github.com/GoogleCloudPlatform/gke-mcp "$REPO_DIR"
else
  echo "gke-mcp already cloned."
fi

cd "$REPO_DIR"
git fetch origin
git checkout "$VERSION"

echo "Installing UI dependencies..."
npm --prefix ui install

echo "Building UI..."
npm --prefix ui run build

echo "Building gke-mcp..."
go build -o gke-mcp .

echo "Setup complete. Binary is at $REPO_DIR/gke-mcp"
