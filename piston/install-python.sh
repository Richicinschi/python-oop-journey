#!/bin/bash
# Install Python runtime in Piston
# Run this after Piston container is deployed

echo "Installing Python 3.12.0 runtime in Piston..."

# Install Python runtime
ppman install python 3.12.0

echo "Python runtime installed successfully!"
echo ""
echo "Verifying installation..."
curl -s http://localhost:2000/api/v2/runtimes | grep python
