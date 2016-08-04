//
//  VarianceCovariance.hpp
//  
//
//  Created by Dimitar Ananiev Popov on 21/03/16.
//
//

// Idea: Create a class which takes input
// -> TimeSeries objects
// -> Given above, create data matrix
// -> Given data matrix, calculate Var/Covar matrix
// Idea: Tobias & Pascal suggested BLAS, BOOST
// Idea: Tobias suggested to create vector of vectors or
// -> vector of objects (unsure of how)

#pragma once

#include <vector>
#include <string>
#include <Eigen/Dense>

using std::vector; 
using Eigen::MatrixXd;

class VarianceCovariance
{
private:
    // Variables
    Eigen::MatrixXd varCovarMatrix_;
public:
    
    // Constructor
    // Default Cons.
    VarianceCovariance();
    /* Overloaded Cons.
    VarianceCovariance(Eigen::MatrixXd varianceCovarianceMatrix);
    */
    
    // Destructor
    ~VarianceCovariance();

    // Methods
    void makeVarCovarMatrix(std::string filePath, std::string fileName);

    // Accessors
    Eigen::MatrixXd getVarCovarMatrix(std::string filePath, std::string fileName);
    
};

