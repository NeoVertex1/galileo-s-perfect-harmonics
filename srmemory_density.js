const math = require('mathjs');

// Constants
const psi = 44.8, xi = 3721.8, tau = 64713.97, epsilon = 0.28082;
const phi = (1 + Math.sqrt(5)) / 2;

// 1. Test Memory Density
const memoryDensity = tau * phi / (psi * epsilon);
console.log("Memory Density (bits/state):", math.log(memoryDensity) / math.log(2));

// 2. Test Phase Transitions
const T_c = psi * phi / epsilon;
const transitionPoints = [];
for(let i = 0; i < 5; i++) {
    transitionPoints.push(tau / math.pow(phi, i));
}
console.log("\nPhase Transition Points:", transitionPoints);

// 3. Test Error Suppression
function errorSuppressionFactor(dimension) {
    return math.exp(-epsilon * epsilon * dimension / (psi * phi));
}
const errorFactors = Array.from({length: 5}, (_, i) => errorSuppressionFactor(i + 1));
console.log("\nError Suppression Factors:", errorFactors);

// 4. Test Manifold Structure
function calculateManifoldProperties(dim) {
    const stablePoints = psi * Math.pow(phi, dim);
    const connectionDensity = tau/dim;
    const topologicalInvariant = math.exp(-dim * epsilon / psi);
    return {dim, stablePoints, connectionDensity, topologicalInvariant};
}

const manifoldResults = Array.from({length: 4}, (_, i) => 
    calculateManifoldProperties(i + 1));
console.log("\nManifold Properties:", manifoldResults);

// 5. Test Coherence Times
function predictCoherenceTime(systemSize) {
    return tau * math.exp(-systemSize * epsilon / (psi * phi));
}
const coherenceTimes = Array.from({length: 5}, (_, i) => 
    predictCoherenceTime(Math.pow(2, i)));
console.log("\nPredicted Coherence Times:", coherenceTimes);
