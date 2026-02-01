#pragma endian big

import std.sys;
import std.mem;
import std.string;

struct Header {
    char mMagic[4]; // MNCH
    u32 mEntryOffset;
    u32 mFlags;
    u32 mCurveEntryCount;
    u32 m_10;
    s16 m_14;
    bool m_16;
    padding[1];
};

struct ControlPoint {
    s16 x;
    s16 y;
    s16 z;
    s16 w;
};

struct CurveBlock {
    u32 m_0;
    u32 m_4;
    s32 m_8;
    u32 mControlPointOffset;
    u32 mKnotOffset;
    u32 m_14;
    float m_18[8]; // transforms?
    u32 mNumControlPoints;
    ControlPoint mControlPoints[mNumControlPoints];
    u32 mNumKnots;
    float mKnots[mNumKnots];
    u32 m_unk_NextOffset;
    u8 m_unk_data[(m_unk_NextOffset - $)]; // anim data?
    u32 mUnk2;
    u32 mUnkArray2[mUnk2];
};

struct Transform {
    s16 m_0;
    s16 m_2;
    s16 m_4;
    s16 m_8;
};

struct PointTransform {
    u16 mControlPointIndex;
    u16 mNumTransforms;
    
    Transform mTransforms[mNumTransforms];
};

struct PointTransformPointer {
    PointTransform* ptr : u32;
};

struct CurveEntry {
    char mMagic[4]; // MNCN
    u32 mEntrySize;
    char mName[0x20];
    u8 m_28[0x64];
    float m_8C;
    u32 m_90;
    u32 m_94;
    u32 m_98;
    u32 mControlPointOffset;
    u32 mKnotOffset;
    u32 mPointTransformOffset;
    float m_A8[4];
    u32 m_B8[4];
    u32 mNumControlPoints;
    ControlPoint mControlPoints[mNumControlPoints];
    u32 mNumKnots;
    float mKnots[mNumKnots];
    u32 m_unk_NextOffset;
    padding[(m_unk_NextOffset - $)]; // anim data?
    u32 mNumPointTransforms;
    PointTransformPointer mPointTransforms[mNumPointTransforms];
};

struct DemoOption {
    char mName[0x10];
    u32 mNumUsedValues;
    u8 mValues[mNumUsedValues];
    // the next DemoOption is padded to a multiple of 4 that
    // *isn't* directly after the end of this struct/
    // e.g. if this struct ends at _4 (as in, the final value is *ON* _3),
    // the next DemoOption will start at _8 instead
};

struct DemoOptionPointer {
    DemoOption* ptr : u32;
};

struct DemoOptionSet {
    char mName[0x20];
    char m_20[0x20];
    u32 mNumOptions;
    DemoOptionPointer mDemoOptions[mNumOptions];
};

struct DemoOptionSetPointer {
    DemoOptionSet* ptr : u32;
};

struct DemoData {
    char mMagic[4];
    u32 mEntrySize;
    u32 mNumDemoOptionSets;
    DemoOptionSetPointer mDemoOptionSets[mNumDemoOptionSets];
};

Header header @ 0;
CurveEntry entries[header.mCurveEntryCount] @ header.mEntryOffset;
//DemoData dd @ header.mEntryOffset;
