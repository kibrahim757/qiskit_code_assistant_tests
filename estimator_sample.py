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
# Transpile the circuit using a preset pass manager
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)
# Transpile the circuit
transpiled_circuit = pm.run(qc)
# Create an estimator instance
estimator = Estimator(mode=backend)
# Estimate the expectation value of the measurement
job = estimator.run([transpiled_circuit],[ZZ])
# Get the results
results = job.result()
# Plot the histogram of results using cregisters
counts = results[0].data.c.get_counts()
# Plot the histogram
plot_histogram(counts, title="Entanglement Measurement Results")
# Note: The EstimatorV2 is used here for estimating expectation values, which is different from sampling.
# If you want to sample the results, you would typically use a SamplerV2 instead. 