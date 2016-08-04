/* Own includes */
#include "ProblemQP.h"

/* KNITRO includes */ 
#include "KTRSolver.h"
#include "ExampleHelpers.h"

/* An example of loading and solving a problem using exact gradient and and Hessian evaluations.
 * When using exact derivative evaluations, no KTR_GRADOPT_* or KTR_HESSOPT_* parameter is needed.
 */
int main() {
  // Create a problem instance.
  ProblemQP instance = ProblemQP();
  instance.prepareProblemQP();

  // Create a solver
  knitro::KTRSolver solver(&instance);

  int solveStatus = solver.solve();

  printSolutionResults(solver, solveStatus);

  return 0;
}
