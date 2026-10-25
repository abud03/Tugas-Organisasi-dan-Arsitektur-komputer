# Simulator from https://github.com/harshitasingh4863/instruction-level-parallelism-simulator.git

from dataclasses import dataclass
import matplotlib.pyplot as plt
import networkx as nx


@dataclass
class Instruction:
    name: str
    destination: str
    sources: list


# -------------------------------------------------
# Sample Instruction Set
# -------------------------------------------------

instructions = [
    Instruction("I1", "R1", ["R2", "R3"]),
    Instruction("I2", "R4", ["R5", "R6"]),
    Instruction("I3", "R7", ["R1", "R4"]),
    Instruction("I4", "R8", ["R9", "R10"]),
    Instruction("I5", "R11", ["R7", "R8"]),
    Instruction("I6", "R12", ["R13", "R14"]),
    # Menambahkan instruksi tambahan untuk memicu dependensi WAW
    Instruction("I7", "R1", ["R11", "R12"]),
]


# -------------------------------------------------
# Functions to check dependencies
# -------------------------------------------------

def has_raw_dependency(inst1, inst2):
    """
    Returns True if inst2 depends on inst1 (Read-After-Write).
    """
    if inst1.destination in inst2.sources:
        return True
    return False


def has_waw_dependency(inst1, inst2):
    """
    Returns True if inst2 writes to the same register as inst1 (Write-After-Write).
    """
    if inst1.destination == inst2.destination:
        return True
    return False


# -------------------------------------------------
# Sequential Execution
# -------------------------------------------------

def sequential_execution(instructions):
    print("\n" + "=" * 50)
    print("SEQUENTIAL EXECUTION")
    print("=" * 50)

    cycle = 0

    for instruction in instructions:
        cycle += 1

        print(
            f"Cycle {cycle}: Executing {instruction.name} "
            f"({instruction.destination} = "
            f"{' + '.join(instruction.sources)})"
        )

    print(f"\nTotal Sequential Cycles: {cycle}")

    return cycle


# -------------------------------------------------
# ILP / Parallel Execution
# -------------------------------------------------

def parallel_execution(instructions):
    print("\n" + "=" * 50)
    print("INSTRUCTION-LEVEL PARALLEL EXECUTION (RAW & WAW Constraints)")
    print("=" * 50)

    completed = set()
    remaining = instructions.copy()

    cycle = 0

    while remaining:

        cycle += 1
        current_cycle = []

        for instruction in remaining:

            dependencies_satisfied = True

            for previous in instructions:

                if previous.name == instruction.name:
                    break

                # Cek dependensi RAW dan WAW
                if has_raw_dependency(previous, instruction) or has_waw_dependency(previous, instruction):
                    if previous.name not in completed:
                        dependencies_satisfied = False
                        break

            if dependencies_satisfied:
                current_cycle.append(instruction)

        print(f"\nCycle {cycle}:")

        for instruction in current_cycle:
            print(
                f"  -> {instruction.name}: "
                f"{instruction.destination} = "
                f"{' + '.join(instruction.sources)}"
            )

        for instruction in current_cycle:
            completed.add(instruction.name)
            remaining.remove(instruction)

    print(f"\nTotal ILP Cycles: {cycle}")

    return cycle


# -------------------------------------------------
# Dependency Analysis & Graph Generation
# -------------------------------------------------

def analyze_and_draw_dependencies(instructions):
    print("\n" + "=" * 50)
    print("DEPENDENCY ANALYSIS")
    print("=" * 50)

    # Inisialisasi graph berarah (Directed Graph)
    G = nx.DiGraph()
    
    # Tambahkan semua node instruksi
    for inst in instructions:
        G.add_node(inst.name)

    edge_labels = {}
    raw_edges = []
    waw_edges = []

    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            
            # Deteksi RAW
            if has_raw_dependency(instructions[i], instructions[j]):
                print(f"[RAW] {instructions[j].name} depends on {instructions[i].name} (Register: {instructions[i].destination})")
                G.add_edge(instructions[i].name, instructions[j].name)
                raw_edges.append((instructions[i].name, instructions[j].name))
                edge_labels[(instructions[i].name, instructions[j].name)] = f"RAW ({instructions[i].destination})"

            # Deteksi WAW
            if has_waw_dependency(instructions[i], instructions[j]):
                print(f"[WAW] {instructions[j].name} writes after {instructions[i].name} (Register: {instructions[i].destination})")
                G.add_edge(instructions[i].name, instructions[j].name)
                waw_edges.append((instructions[i].name, instructions[j].name))
                edge_labels[(instructions[i].name, instructions[j].name)] = f"WAW ({instructions[i].destination})"

    # Menggambar Dependency Graph
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)
    
    # Gambar node
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Gambar garis relasi/dependensi
    nx.draw_networkx_edges(G, pos, edgelist=raw_edges, edge_color='red', width=2, arrowstyle='->', arrowsize=20, label='RAW')
    nx.draw_networkx_edges(G, pos, edgelist=waw_edges, edge_color='orange', width=2, arrowstyle='->', arrowsize=20, label='WAW')
    
    # Label garis
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, font_color='black')
    
    plt.title("Instruction-Level Dependency Graph (RAW & WAW)", fontsize=14, fontweight='bold')
    plt.legend(loc='upper right')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# -------------------------------------------------
# Main Program
# -------------------------------------------------

def main():
    print("\n")
    print("*" * 60)
    print("      INSTRUCTION-LEVEL PARALLELISM SIMULATOR (WAW INCLUDED)")
    print("*" * 60)

    print("\nInstruction Set:")
    for instruction in instructions:
        print(
            f"{instruction.name}: "
            f"{instruction.destination} = "
            f"{' + '.join(instruction.sources)}"
        )

    # Analisis dependensi & menggambar Graph
    analyze_and_draw_dependencies(instructions)

    # Sequential execution
    sequential_cycles = sequential_execution(instructions)

    # Parallel execution
    parallel_cycles = parallel_execution(instructions)

    # Calculate speedup
    speedup = sequential_cycles / parallel_cycles
    efficiency = speedup / len(instructions) * 100

    print("\n" + "=" * 50)
    print("PERFORMANCE COMPARISON")
    print("=" * 50)
    print(f"Sequential Cycles : {sequential_cycles}")
    print(f"ILP Cycles        : {parallel_cycles}")
    print(f"Speedup            : {speedup:.2f}x")
    print(f"ILP Efficiency     : {efficiency:.2f}%")


if __name__ == "__main__":
    main()
