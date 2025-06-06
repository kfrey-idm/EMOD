
#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <memory> // unique_ptr
#include "UnitTest++.h"
#include "WaningEffectMap.h"
#include "componentTests.h"

using namespace Kernel; 



SUITE(WaningEffectMapTest)
{
    TEST(TestPiecewiseGetMultiplier)
    {
        unique_ptr<Configuration> p_config( Environment::LoadConfigurationFile( "testdata/WaningEffectMapTest.json" ) );

        WaningEffectMapPiecewise piecewise;

        piecewise.Configure( p_config.get() );

        CHECK_EQUAL( 1.0f, piecewise.GetMultiplier( 0.0f ) );
        CHECK_EQUAL( 1.0f, piecewise.GetMultiplier( 0.5f ) );
        CHECK_EQUAL( 1.0f, piecewise.GetMultiplier( 1.0f ) );
        CHECK_EQUAL( 1.0f, piecewise.GetMultiplier( 1.5f ) );
        CHECK_EQUAL( 3.0f, piecewise.GetMultiplier( 2.0f ) );
        CHECK_EQUAL( 3.0f, piecewise.GetMultiplier( 2.5f ) );
        CHECK_EQUAL( 5.0f, piecewise.GetMultiplier( 3.0f ) );
        CHECK_EQUAL( 5.0f, piecewise.GetMultiplier( 3.5f ) );
        CHECK_EQUAL( 7.0f, piecewise.GetMultiplier( 4.0f ) );
        CHECK_EQUAL( 7.0f, piecewise.GetMultiplier( 4.5f ) );
        CHECK_EQUAL( 5.0f, piecewise.GetMultiplier( 5.0f ) );
        CHECK_EQUAL( 5.0f, piecewise.GetMultiplier( 5.5f ) );
        CHECK_EQUAL( 3.0f, piecewise.GetMultiplier( 6.0f ) );
        CHECK_EQUAL( 1.0f, piecewise.GetMultiplier( 6.5f ) );
        CHECK_EQUAL( 1.0f, piecewise.GetMultiplier( 7.0f ) );
    }
}