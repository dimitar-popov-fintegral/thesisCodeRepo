//
//  TimeSeriesReadCSV.hpp
//  
//
//  Created by Dimitar Ananiev Popov on 27/03/16.
//
//

#pragma once

#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using std::string; using std::vector;

class TimeSeriesReadCSV
{
private:
    const std::string filePath_;
    const std::string fileName_;
    std::vector<std::string> isinToStringVector_;
    std::vector<std::vector<std::string> > matrixDates_;
    std::vector<std::vector<double> > matrixData_;
public:
    // Constructor
    // Default
    TimeSeriesReadCSV();
    
    // Overloaded
    TimeSeriesReadCSV(std::string filePath,
                      std::string fileName);
    
    // Destructor
    ~TimeSeriesReadCSV();
    
    // Methods
    int readNumberOfLines();
    int readNumberOfColumns();
    void copySaveFile();
    void readIsin(); 
    void readData();

    // Accessors
    std::vector<std::string> getIsin();
    std::vector<std::vector<double> > getData();
    std::vector<std::vector<std::string>  > getDates();
};

