# Sum Fuel requirements
# https://adventofcode.com/2019/day/1
import fileinput


def calc_fuel_requirement_recursively(mass: int) -> int:
    result = 0
    while mass > 0:
        fuel = calc_fuel_requirement(mass)
        result += fuel
        mass = fuel
    return result


def calc_fuel_requirement(mass: int) -> int:
    return max(0, mass // 3 - 2)


def main():
    masses = [int(line) for line in fileinput.input()]
    fuel_requirements = [
        calc_fuel_requirement_recursively(mass) for mass in masses]
    print(sum(fuel_requirements))


if __name__ == "__main__":
    main()
