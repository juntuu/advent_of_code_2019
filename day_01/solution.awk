#!/usr/bin/awk -f


{ total += int($1 / 3) - 2 }

END { print "Day 1, part 1:", total }

