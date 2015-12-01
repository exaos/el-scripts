#!/bin/bash

git update-index --index-version 4
GIT_INDEX_FILE=.git/annex/index git update-index --index-version 4
git config gc.auto 0

# git count-objects

# git repack -d
# git gc
# git prune
