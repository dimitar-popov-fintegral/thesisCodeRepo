/*******************************************************/
/* Copyright (c) 2015 by Artelys                       */
/* All Rights Reserved                                 */
/*******************************************************/

#include "KTRSolver.h"

#include "ProblemHS15.h"
#include "ExampleHelpers.h"

/**
 * An example of loading and solving a problem using exact gradient and and Hessian evaluations.
 * When using exact derivative evaluations, no KTR_GRADOPT_* or KTR_HESSOPT_* parameter is needed.
 */
int main() {
  // Create a problem instance.
  ProblemHS15 instance = ProblemHS15();

  // Create a solver
  knitro::KTRSolver solver(&instance);

  int solveStatus = solver.solve();

  printSolutionResults(solver, solveStatus);

  return 0;
}
