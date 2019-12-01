#!/usr/bin/awk -f


function fuel_for_mass(m) {
	return int(m / 3) - 2
}

{
	module = fuel_for_mass($1)
	total += module
	fuel = fuel_for_mass(module)
	while (fuel > 0) {
		total_fuel += fuel
		fuel = fuel_for_mass(fuel)
	}
}

END {
	print "Day 1, part 1:", total
	print "Day 1, part 2:", total + total_fuel
}

