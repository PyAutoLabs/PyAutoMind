#!/usr/bin/env bash
# Forwarding shim — health_release.sh moved to PyAutoHeart/scripts/ (the Heart owns the
# health surface; Mind stores intent). Point your sourcing at the new home;
# this shim keeps old paths working.
source "$(dirname "${BASH_SOURCE[0]}")/../../PyAutoHeart/scripts/health_release.sh"
