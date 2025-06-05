from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
# Initialize the Qiskit Runtime Service
service = QiskitRuntimeService(channel="ibm_cloud", instance="crn:v1:bluemix:public:quantum-computing:us-east:a/ba962309ce1047b196c3c050588a6d71:8fda7a93-e60c-4a4c-ba5b-6d1e5262669c::", token="5iN_CtEVi_QxhMiBnsbIacmxY57F5y4iCzhbaatYPE_A")
backend = service.least_busy()
print(f"Using backend: {backend.name}")
# Create a quantum circuit for entanglement and measurement then draw it
qc = QuantumCircuit(2, 2)
qc.h(0)  # Apply Hadamard gate to qubit 0
qc.cx(0, 1)  # Apply CNOT gate to entangle qubit 0 and qubit 1
qc.measure([0, 1], [0, 1])  # Measure both qubits
qc.draw("mpl")
# set observables for the expectation value
from qiskit.quantum_info import SparsePauliOp
ZZ = SparsePauliOp.from_list([("ZZ", 1)])  # Define the observable for ZZ measurement
# Note: The SparsePauliOp is used to define the observable for expectation value estimation.
# If you want to sample the results, you would typically use a different observable or measurement setup.
# Transpile the circuit using a preset pass manager
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
# Transpile the circuit
transpiled_circuit = pm.run(qc)
# Create an estimator instance
estimator = Estimator(backend=backend)
# map observables to the circuit
observables = [ZZ.apply_layout(transpiled_circuit.layout)]
# run estimator to get the expectation value
job = estimator.run([(transpiled_circuit, observables)])
# Get the results
results = job.result()
# Get estimator results
from matplotlib import pyplot as plt
values = results[0].data.evs
errors = results[0].data.stds
# plotting graph
plt.plot(["ZZ"], values, "-o")
plt.xlabel("Observables")
plt.ylabel("Values")
plt.show()