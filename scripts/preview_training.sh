#!/usr/bin/env bash
#
# Preview this site locally with the training lessons pulled from any branch of
# Eco-Flow/training — useful for reviewing lesson changes before they are merged.
#
#   scripts/preview_training.sh                    # lessons from main
#   scripts/preview_training.sh split-hpc-modules  # lessons from a branch
#
# Needs Ruby + bundler (see test_locally.md) and Python 3.

set -euo pipefail
cd "$(dirname "$0")/.."

export TRAINING_REF="${1:-main}"

echo "▶ Syncing lessons from Eco-Flow/training @ ${TRAINING_REF}"
python3 -c "import yaml" 2>/dev/null || pip3 install --quiet PyYAML
python3 scripts/sync_training.py

echo
echo "▶ Note: this rewrites _training/ and assets/training/. To undo afterwards:"
echo "    git checkout -- _training assets/training"
echo
echo "▶ Building — the course will be at http://localhost:4000/training/"
bundle exec jekyll serve --livereload
