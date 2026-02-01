#pragma once

#include <cstdint>

// used to indicate that an array is variable-length
#define UNDEFINED_SIZE 1

// all offsets are relative to the start of the file.
using Offset = uint32_t;

// Size: 0x18
struct Header {
    /* 0x00 */ char mMagic[4];              // MNCH
    /* 0x04 */ Offset mCurveEntryOffset;
    /* 0x08 */ uint32_t m_8;                // flags? not sure.
    /* 0x0C */ uint32_t mNumCurveEntries;
    /* 0x10 */ uint32_t m_10;
    /* 0x14 */ int16_t mNumFrames;
    /* 0x16 */ bool mIsVisible;
};

/* Demo */

struct DemoOption {
    /* 0x00 */ char mName[0x10];
    /* 0x10 */ uint32_t mNumUsedValues;
    /* 0x14 */ uint8_t mValues[/* mNumUsedValues */ UNDEFINED_SIZE];
};

struct DemoOptionSet {
    /* 0x00 */ char mName[0x20];
    /* 0x20 */ char m_20[0x20];
    /* 0x40 */ uint32_t mNumOptions;
    /* 0x44 */ Offset mDemoOptionOffsets[/* mNumOptions */ UNDEFINED_SIZE];
};

struct DemoDataBlock {
    /* 0x0 */ char mMagic[4]; // MNDD
    /* 0x4 */ uint32_t mBlockSize;
    /* 0x8 */ uint32_t mNumDemoOptionSets;
    /* 0xC */ Offset mDemoOptionSetOffsets[/* mNumDemoOptionSets */ UNDEFINED_SIZE];
};

/* Curve */

// Size: 0x8
struct ControlPoint {
    /* 0x0 */ int16_t x;
    /* 0x2 */ int16_t y;
    /* 0x4 */ int16_t z;
    /* 0x6 */ int16_t w;
};

// Size: 0x8
struct KeyFrame {
    int16_t frame;
    bool active;
    /* padding of 1*/
    int16_t x;
    int16_t y;
};

struct CurveBlock {
    /* 0x00 */ char mMagic[4]; // MNCN
    /* 0x04 */ uint32_t mBlockSize;
    /* 0x08 */ char mName[0x20];
    /* 0x28 */ uint8_t m_28[0x64];
    /* 0x8C */ float m_8C;
    /* 0x90 */ uint32_t m_90;
    /* 0x94 */ uint32_t m_94;
    /* 0x98 */ uint32_t m_98;
    /* 0x9C */ Offset mControlPointOffset;
    /* 0xA0 */ Offset mKnotOffset;
    /* 0xA4 */ Offset mAnimationDataOffset;
    /* 0xA8 */ float m_A8[4];
    /* 0xB8 */ uint32_t m_B8[4];
    /* 0xC8 */ uint32_t mNumControlPoints;
    /* 0xCC */ ControlPoint mControlPoints[/* mNumControlPoints */ UNDEFINED_SIZE];
    /* ---- */ uint32_t mNumKnots;
    /* ---- */ float mKnots[/* mNumKnots */ UNDEFINED_SIZE];
    /* ---- */ Offset mTransformTableOffset;
    /* ---- */ uint8_t padding[0xC]; // explicit padding
    /* ---- */ KeyFrame mKeyFrames[UNDEFINED_SIZE];
    /* ---- */ uint32_t mNumKeyFrames;
    /* ---- */ Offset mKeyFrameOffsets[/* mNumKeyFrames */ UNDEFINED_SIZE];
};
