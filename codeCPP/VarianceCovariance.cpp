#include "VarianceCovariance.hpp"
#include "TimeSeriesReadCSV.hpp"

#include <stdio.h>
#include <iostream>
#include <Eigen/Dense>
#include <vector>
#include <string>

using std::string; using std::vector; 
using Eigen::MatrixXd; using Eigen::VectorXd;

// Constructor
// Default
VarianceCovariance :: VarianceCovariance() {
    Eigen::MatrixXd varCovarMatrix_;
} 

/* Overloaded
VarianceCovariance :: VarianceCovariance(Eigen::MatrixXd varianceCovarianceMatrix)
                                         :varianceCovarianceMatrix_(varianceCovarianceMatrix)
{
    
}
*/

// Destructor
VarianceCovariance :: ~VarianceCovariance()
{
    
}

void VarianceCovariance ::  makeVarCovarMatrix(std::string filePath, std::string fileName)
{
    // Read data & obtain infromation regarding TS & populate container
    TimeSeriesReadCSV reader(filePath, fileName);
    int n = reader.readNumberOfLines();
    int t = reader.readNumberOfColumns();
    std::vector<std::vector<double>> data = reader.getData();

    // n:= # of obs. t:= # of TS objects.
    // Matrices to be built: 1, X, X_tilde, Sigma
    // X_tilde = X - 1 * transpose(1) * X
    // Sigma = X_tilde * transpose(X_tilde)
    MatrixXd ones = MatrixXd::Constant(n-1, n-1, 1);
    MatrixXd X(n-1 ,t);      
    MatrixXd X_tilde(n-1, t);
    MatrixXd Sigma(t, t);
    double recipricolCount = 1/((double)n - 1);

    // Populate 
    for(int j = 0; j < t; j++)
    {
        for(int i = 0; i < (n-1); i++)
        {
            X(i,j) = data[j][i];   
        }

    } 

    // Print out X to confirm
    X_tilde = X - ((ones * X) * recipricolCount);
    Sigma = recipricolCount * (X_tilde.transpose() * X_tilde);

    // Store in private variable
    varCovarMatrix_ = Sigma;
}

Eigen::MatrixXd VarianceCovariance :: getVarCovarMatrix(std::string filePath, std::string fileName)
{
    makeVarCovarMatrix(filePath, fileName);
    return varCovarMatrix_;
}


