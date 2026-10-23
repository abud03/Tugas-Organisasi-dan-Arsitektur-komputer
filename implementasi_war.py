
# -*- coding: utf-8 -*-
"""Implementasi WAR (Write After Read) menggunakan Python."""

from dataclasses import dataclass


@dataclass
class Instruction:
    name: str
    destination: str
    sources: list


instructions = [
    Instruction("I1", "R1", ["R2", "R3"]),
    Instruction("I2", "R2", ["R4", "R5"]),
    Instruction("I3", "R3", ["R6", "R7"]),
    Instruction("I4", "R8", ["R9", "R10"]),
]


def detect_war(instructions):
    print("DEPENDENCY ANALYSIS - WAR")
    dependencies = []

    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            first = instructions[i]
            second = instructions[j]

            if second.destination in first.sources:
                dependencies.append((first.name, second.name))
                print(
                    f"{first.name} -> {second.name} "
                    f"(Register: {second.destination})"
                )

    if not dependencies:
        print("No WAR dependencies found.")

    return dependencies


def show_dependency_graph(dependencies):
    print("\nDEPENDENCY GRAPH - WAR")

    if not dependencies:
        print("Tidak ada panah ketergantungan.")
        return

    for source, target in dependencies:
        print(f"{source} ----> {target}")


if __name__ == "__main__":
    war_dependencies = detect_war(instructions)
    show_dependency_graph(war_dependencies)
