#!/bin/bash
# Usage: ./ssh.sh [username] [host] [keyfile]
USERNAME="${1:-root}"
HOST="${2:-103.179.173.10}"
KEYFILE="${3:-./key.pem}"

if [ "$#" -gt 3 ]; then
  echo "Usage: $0 [username] [host] [keyfile]"
  exit 1
fi

ssh -i "$KEYFILE" "$USERNAME@$HOST"
  ssh -i "$KEYFILE" "$USERNAME@$HOST"
else
  ssh "$USERNAME@$HOST"
fi
