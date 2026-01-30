// not necessarily a valid C/++ representation but it gets the point across

#pragma once

#include <cstdint>

#define UNK_SIZE 1

template <typename T>
struct Array {
    uint32_t mCount;
    T mItems[/* mCount */];
};

struct ControlPoint {
    /* 0x00 */ int16_t x;
    /* 0x02 */ int16_t y;
    /* 0x04 */ int16_t z;
    /* 0x06 */ int16_t w; // weight
};

// variable size
struct CurveBlock {
    /* 0x00 */ uint32_t m_0;
    /* 0x04 */ uint32_t m_4;
    /* 0x08 */ uint32_t m_8;
    /* 0x0C */ uint32_t mControlPointOffset;
    /* 0x10 */ uint32_t mKnotOffset;
    /* 0x14 */ uint32_t m_14; // some offset
    /* 0x18 */ float m_18[8]; // transforms?
    /* 0x38 */ Array<ControlPoint> mControlPoints;
    /* 0x?? */ Array<float> mKnots;
    /* 0x?? */ uint32_t mUnk1; // the offset to mUnkArray2. i.e. &mUnkArray2 == (&mUnk1 + mUnk1)
    /* 0x?? */ char mUnkData1[UNK_SIZE]; // maybe it's animation data?
    /* 0x?? */ Array<uint32_t> mUnkArray2;
};

// variable size due to ^
struct CurveEntry {
    /* 0x00 */ char mMagic[4]; // "MNCN"
    /* 0x04 */ uint32_t mCurveSize; // the size of this instance of the structure
    /* 0x08 */ char mName[0x20];
    /* 0x28 */ char m_28[0x68]; // maybe a float array? there's usually a float at the very end
    /* 0x90 */ CurveBlock mCurveBlock;
};

struct Header {
    /* 0x00 */ char mMagic[4]; // "MNCH"
    /* 0x04 */ uint32_t mCurveEntryOffset;
    /* 0x08 */ uint32_t mFlags; // not sure what the flags are though
    /* 0x0C */ uint32_t mCurveEntryCount;
    /* 0x10 */ uint32_t m_10;
    /* 0x14 */ uint32_t m_14;
};

struct MNEBFile {
    /* 0x00 */ Header mHeader;
    /* 0x18 */ CurveEntry mCurveEntries[/* mHeader.mCurveEntryCount */];
};

