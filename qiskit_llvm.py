from qiskit import QuantumCircuit
from llvmlite import ir

# Map Qiskit gate names to QIR function names
QIR_GATE_MAP = {
    "h": ("__quantum__qis__h__body", [1]),
    "cx": ("__quantum__qis__cnot__body", [2]),
    "x": ("__quantum__qis__x__body", [1]),
    "z": ("__quantum__qis__z__body", [1]),
    "measure": ("__quantum__qis__mz__body", [1]),
}

def qiskit_to_qir(qc: QuantumCircuit) -> str:
    """Convert a Qiskit QuantumCircuit into a QIR (LLVM IR string)."""

    # Create a new LLVM module
    module = ir.Module(name="qir_module")

    # Define opaque types
    qubit_type = ir.PointerType(ir.IntType(8))   # %Qubit*
    result_type = ir.PointerType(ir.IntType(8))  # %Result*

    # Declare runtime functions (just the ones we need)
    qalloc_ty = ir.FunctionType(qubit_type, [])
    qalloc = ir.Function(module, qalloc_ty, name="__quantum__rt__qubit_allocate")

    # Keep a registry for declared functions
    declared_funcs = {
        "__quantum__rt__qubit_allocate": qalloc
    }

    def get_or_declare(fname, rettype, argtypes):
        if fname in declared_funcs:
            return declared_funcs[fname]
        fnty = ir.FunctionType(rettype, argtypes)
        fn = ir.Function(module, fnty, name=fname)
        declared_funcs[fname] = fn
        return fn

    # Create main function
    main_ty = ir.FunctionType(ir.VoidType(), [])
    main = ir.Function(module, main_ty, name="main")
    block = main.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    # Allocate qubits
    qubits = []
    for _ in range(qc.num_qubits):
        qubits.append(builder.call(qalloc, [], name=f"q{len(qubits)}"))

    # Process operations
    for inst, qargs, cargs in qc.data:
        name = inst.name.lower()
        if name not in QIR_GATE_MAP:
            raise NotImplementedError(f"Gate {name} not yet supported")

        fname, info = QIR_GATE_MAP[name]

        if name == "measure":
            q = qubits[qargs[0].index]
            mz_fn = get_or_declare(fname, result_type, [qubit_type])
            builder.call(mz_fn, [q], name=f"r{cargs[0].index}")
        elif info[0] == 1:
            q = qubits[qargs[0].index]
            fn = get_or_declare(fname, ir.VoidType(), [qubit_type])
            builder.call(fn, [q])
        elif info[0] == 2:
            q0 = qubits[qargs[0].index]
            q1 = qubits[qargs[1].index]
            fn = get_or_declare(fname, ir.VoidType(), [qubit_type, qubit_type])
            builder.call(fn, [q0, q1])
        else:
            raise RuntimeError("Unsupported arity in map")

    builder.ret_void()
    return str(module)


# Example Qiskit circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0,1], [0,1])

print(qiskit_to_qir(qc))
