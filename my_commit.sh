#!/bin/bash

comment=$1
comment="$1 #comment $2"
echo $comment
git add .
git commit --author="alexandrosv <alex@mail.com>" -m "$comment"
git push

#For smart commits:
#./mycommit.sh <jira ticket> "Deleted debugging prints."
