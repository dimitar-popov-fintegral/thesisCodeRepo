/*******************************************************/
/* Copyright (c) 2015 by Artelys                       */
/* All Rights Reserved                                 */
/*******************************************************/
#ifndef _EXAMPLEOUTPUTREDIRECT_H_
#define _EXAMPLEOUTPUTREDIRECT_H_

#include <string>
#include <iostream>
#include "KTRSolver.h"
#include "KTRPutString.h"

/**
 * An example of implementing output redirection. Writes KNITRO output to stderr instead of the default stdout.
 */
class ExampleOutputRedirection : public knitro::KTRPutString {
 public:

  int CallbackFunction(const std::string &str, knitro::KTRSolver * solver)
  {
    std::cerr << str;

    return static_cast<int>(str.length());
  }
};

#endif
