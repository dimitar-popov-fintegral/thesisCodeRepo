//
//  TimeSeriesReadCSV.cpp
//  
//
//  Created by Dimitar Ananiev Popov on 27/03/16.
//
//

#include "TimeSeriesReadCSV.hpp"

#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <iterator>
#include <regex>
#include <boost/tokenizer.hpp>

using std::string; using std::vector; using std::ifstream;


// Structs
struct HasEmpty
{
    bool operator()(const std::string& s)
    {
        return s.find(';', 0) != std::string::npos;
    }
};

// Constructior
// Overloaded
TimeSeriesReadCSV :: TimeSeriesReadCSV(std::string filePath, std::string fileName)
                                        : filePath_(filePath),fileName_(fileName)
{
    
}

// Destructor
TimeSeriesReadCSV :: ~TimeSeriesReadCSV()
{
    
}

// Methods

std::vector<double> castStringToDouble(const std::vector<std::string>& stringVector)
{
    // Construct doubleVector to be cast from stringVector
    std::vector<double> doubleVector(stringVector.size());
    std::transform(stringVector.begin(), stringVector.end(), doubleVector.begin(), [](const std::string& val)
                     {
                         return stod(val);
                     });
    return doubleVector;
}

int TimeSeriesReadCSV :: readNumberOfLines()
{
    std::string myfileName = filePath_ + fileName_;
    std::ifstream myfile(myfileName);
    uint16_t line_count;

    if(!myfile.is_open())
    {
        std::cout << "File:" + myfileName << std::endl;
        std::cout << "File Open: Failed" << std::endl;
    }
    else
    {
        // new lines will be skipped unless we stop it from happening:
        myfile.unsetf(std::ios_base::skipws);
        
        // count the newlines with an algorithm specialized for counting:
        line_count = std::count(std::istream_iterator<char>(myfile),
                                 std::istream_iterator<char>(),
                                 '\n');
    }
    
    myfile.close();
    return line_count;
}

int TimeSeriesReadCSV :: readNumberOfColumns()
{
    std::string myfileName = filePath_ + fileName_;
    std::ifstream myfile(myfileName);
    uint16_t count, col_count;
    
    if(!myfile.is_open())
    {
        std::cout << "File:" + myfileName << std::endl;
        std::cout << "File Open: Failed" << std::endl;
    }
    else
    {
        std::string testLine;
        std::getline(myfile, testLine, '\n');
        std::cout << testLine << std::endl;
        count = std::count(testLine.begin(), testLine.end(), ',');
        col_count = ((count-1) / 3) + 1;
        
        if(!isdigit(col_count))
        {
            col_count = floor(col_count);
        }
    }
    
    myfile.close();
    return col_count;
}

void TimeSeriesReadCSV :: copySaveFile()
{
    std::string myfileName = filePath_ + fileName_;
    std::string myfileTarget = filePath_ + "mod_" + fileName_;

    std::ifstream  src(myfileName, std::ios::binary);
    std::ofstream  dst(myfileTarget, std::ios::binary);

    dst << src.rdbuf();
}

void TimeSeriesReadCSV :: readIsin()
{
    // Construct some containers
    std::vector<std::string> isin;

    // Open modification file with ifstream (with full path)
    std::cout << "Reading from: " + filePath_ + fileName_ << std::endl;
    copySaveFile();
    std::string myfileTarget = filePath_ + "mod_" + fileName_;
    std::ifstream myfile(myfileTarget);
    std::cout << "Writing to: " + myfileTarget << std::endl;

    // Check if file is open
    if(!myfile.is_open())
    {
        std::cout << "File:" + myfileTarget << std::endl;
        std::cout << "File Open: Failed" << std::endl;
    }
    else
    {
        std::cout << "File Open: Success" << std::endl;

        // Read first line string
        std::string isinLine;
        std::getline(myfile, isinLine, '\n');

        // Strip ",,," -> replace with "  "
        std::cout << "original: " + isinLine << std::endl;
        std::regex regExpression ("\\,{3}|\\,{1}\n");
        isinLine = std::regex_replace (isinLine, regExpression, "  ");
        std::cout << "original: " + isinLine << std::endl;

        // Construct vector to populate
        std::vector<std::string> isinToStringVector;
        while(isinLine[0] != ',') // old::isinLine.compare(",") != 0
        {
            std::cout << "test: " + isinLine << std::endl;
            std::regex regExpression ("^(.*?)\\s\\s"); //new::^(.*?)\s\s old::^([^,]+)\\s\\s
            std::smatch matchIsin;

            // Search for match using Regex
            std::regex_search(isinLine, matchIsin, regExpression);

            // Check if last ISIN: Pattern is different 
            if(matchIsin.empty())
            {
                std::cout << "Final ISIN Reached:" << std::endl;
                std::regex regExpression ("^(.*?),"); //new::^(.*?)\s\s old::^([^,]+)\\s\\s
                std::smatch matchIsin;
                std::regex_search(isinLine, matchIsin, regExpression);
                isinToStringVector.push_back(matchIsin[0]);
                std::cout << "match: " << matchIsin[0] << std::endl;

                // Erase match from original(isinString)
                isinLine = std::regex_replace (isinLine, regExpression, ",");
            }
            else
            {
                isinToStringVector.push_back(matchIsin[0]);
                std::cout << "match: " << matchIsin[0] << std::endl; // Note that match includes two empty spaces at the end ->> toFix!

                // Erase match from original(isinString)
                isinLine = std::regex_replace (isinLine, regExpression, "");   
            }
        }
        isinToStringVector_ = isinToStringVector;
    }
}

void TimeSeriesReadCSV :: readData()
{
    std::vector<std::string> newLine;

    // Open modification file with ifstream (with full path)
    std::cout << "Reading from: " + filePath_ + fileName_ << std::endl;
    copySaveFile();
    std::string myfileTarget = filePath_ + "mod_" + fileName_;
    std::ifstream myfile(myfileTarget);
    std::cout << "Writing to: " + myfileTarget << std::endl;

    // Check if file is open
    if(!myfile.is_open())
    {
        std::cout << "File:" + myfileTarget << std::endl;
        std::cout << "File Open: Failed" << std::endl;
    }
    else
    {
        std::cout << "File Open: Success" << std::endl;

        // Get critical parameters of .csv file
        int n = readNumberOfLines();
        int t = readNumberOfColumns();

        // Set up some containers
        std::string headerLine;
        std::string line;
        std::vector<std::vector<std::string>> dataVec;

        // Boost elements define
        typedef boost::escaped_list_separator<char> Separator;
        typedef boost::tokenizer<Separator> Tokenizer;

        // Ignore first two lines; they are read elsewhere
        std::getline(myfile, headerLine); // first line
        std::getline(myfile, headerLine); // second line

        // Begin read .csv file
        while (std::getline(myfile, line))
        {
            std::vector<std::string> tokens;
            Tokenizer tokenizer(line);
            for (auto &token : tokenizer)
            {
               tokens.push_back(token);
               //tokens.erase(std::remove_if(tokens.begin(), tokens.end(), HasEmpty()), tokens.end()); 
            }

            dataVec.push_back(tokens);

            /* Test: 
            if(std::cout << dataVec[1].size() << std::endl;) == readNumberOfColumns()*3 - 1
            */
        }

        /* Test: given test .csv           
        std::cout << dataVec[0][0] << std::endl; == 1/12/2016 (first value)
        std::cout << dataVec[0][1] << std::endl; == 64.83
        std::cout << dataVec[22][4] << std::endl; == 18.18 (last value)
        */

        // Construct vector to fill with vectors of timeSeries
        std::vector<std::vector<std::string> > matrixDates;
        std::vector<std::vector<double> >      matrixData;

        for (int i = 0; i < ((t*3)-1); i=i+3)
        {
            std::vector<std::string> tempDates;
            std::vector<std::string> tempData;
            for (int j = 0; j <= (n-2); ++j)
            {  
                tempDates.push_back(dataVec[j][i]);
                tempData.push_back(dataVec[j][i+1]);
            }
            // Push dates as-is
            matrixDates.push_back(tempDates);
            // Push data requires type conversion to double
            matrixData.push_back(castStringToDouble(tempData));
        }

        matrixDates_ = matrixDates;
        matrixData_ = matrixData;

        /*
        // Test: Check dimensions of read data
        if (matrixDates.size() != dataVec.size())
        {
            std::cout << "ERROR:Dimension Mis-match" <<std::endl;
            return;
        }
        // Test: Check that correct conversion from raw data has occured 
        if (matrixDates[0][0] != dataVec[0][0] | matrixData[0][0] != dataVec[0][1])
        {
            std::cout << "ERROR:Element-wise Mis-match" <<std::endl;
            return;
        }*/
        
    }
}

std::vector<std::string> TimeSeriesReadCSV :: getIsin()
{
    readIsin();
    return isinToStringVector_;
} 

std::vector<std::vector<double> > TimeSeriesReadCSV :: getData()
{
    readData();
    return matrixData_;         
}

std::vector<std::vector<std::string> > TimeSeriesReadCSV :: getDates()
{
    readData();
    return matrixDates_;         
}
