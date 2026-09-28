# 6 個核心 MapleStory 函數 Decompiled Pseudocode

> **來源**: `wf-output/ida-v83-direct/decompiles.json`
> **工具**: Hex-Rays Decompiler 9.3.0.251224 + goMBA ML

## Packet Dispatcher

### `CLogin::OnPacket` @ `0x5f80ff` (385B → 86 行)

```c
int __thiscall CLogin::OnPacket(char *this, signed int a2, signed int Src)
{
  int result; // eax

  // Credits Sunnyboy @ http://forum.ragezone.com/
  result = a2;
  switch ( a2 )
  {
    case 0:
      result = sub_5F83EE(this - 8, Src);
      break;
    case 1:
      result = sub_5F8F27(Src);
      break;
    case 2:
      result = sub_5F92DF(Src);
      break;
    case 3:
      result = sub_5F92AE(Src);
      break;
    case 4:
      result = sub_5FC731(Src);
      break;
    case 5:
      result = sub_5FC838(Src);
      break;
    case 6:
      result = sub_5FC89D(Src);
      break;
    case 7:
      result = sub_5FCBC1(Src);
      break;
    case 8:
      result = sub_5FACCA(Src);
      break;
    case 9:
      result = sub_5FB245(Src);
      break;
    case 10:
      result = sub_5F95B7(Src);
      break;
    case 11:
      result = sub_5F9891(Src);
      break;
    case 12:
      result = sub_5FB541(Src);
      break;
    case 13:
      result = sub_5F9C72(Src);
      break;
    case 14:
      result = sub_5FA26C(Src);
      break;
    case 15:
      result = sub_5F9D15(Src);
      break;
    case 22:
      result = sub_5FB83D(Src);
      break;
    case 23:
      result = sub_5FB950(Src);
      break;
    case 26:
      result = sub_5F82F4(Src);
      break;
    case 27:
      result = sub_5F8340(Src);
      break;
    case 28:
      result = sub_5FBA49(Src);
      break;
    default:
      if ( a2 < 125 || a2 > 127 )
      {
        if ( a2 >= 128 && a2 <= 130 )
          result = CStage::OnPacket(a2, Src);
      }
      else
      {
        result = sub_775FE6(a2, Src);
      }
      break;
  }
  return result;
}

```

### `CStage::OnPacket` @ `0x644446` (60B → 14 行)

```c
int __stdcall CStage::OnPacket(int a1, int a2)
{
  int result; // eax

  if ( a1 == 128 )
    return sub_6445C5(a2);
  if ( a1 == 129 )
    return sub_6449D2(a2);
  result = a1 - 130;
  if ( a1 == 130 )
    return sub_6449CA(a2);
  return result;
}

```

### `CField::OnPacket` @ `0x531325` (1,201B → 246 行)

```c
int __thiscall CField::OnPacket(char *this, signed int Args, char *Str)
{
  int result; // eax

  // Credits Sunnyboy @ http://forum.ragezone.com/
  result = Args;
  if ( Args > 302 )
  {
    switch ( Args )
    {
      case 303:
        return sub_53347C((char)Str);
      case 309:
        return sub_7C8A4C(Str);
      case 312:
        return sub_73FFF1(Str);
      case 313:
        return sub_8511FC(Str);
      case 314:
        return sub_65DF4C(Str);
      case 322:
        return sub_6F56EA(Str);
      default:
LABEL_35:
        if ( Args < 160 || Args > 235 )
        {
          if ( Args < 236 || Args > 256 )
          {
            if ( Args < 257 || Args > 264 )
            {
              if ( Args < 265 || Args > 267 )
              {
                if ( Args < 268 || Args > 269 )
                {
                  if ( Args < 270 || Args > 272 )
                  {
                    if ( Args < 273 || Args > 274 )
                    {
                      if ( Args < 275 || Args > 276 )
                      {
                        if ( Args < 277 || Args > 280 )
                        {
                          if ( Args == 304 )
                          {
                            return sub_7465F4(304, Str);
                          }
                          else if ( Args < 335 || Args > 337 )
                          {
                            if ( Args < 305 || Args > 306 )
                            {
                              if ( Args < 310 || Args > 311 )
                              {
                                if ( Args < 125 || Args > 127 )
                                {
                                  if ( Args < 128 || Args > 130 )
                                  {
                                    if ( Args < 340 || Args > 345 )
                                    {
                                      if ( Args < 307 || Args > 308 )
                                      {
                                        if ( Args < 349 || Args > 352 )
                                        {
                                          if ( Args < 353 || Args > 356 )
                                          {
                                            if ( Args >= 357 && Args <= 360 )
                                              return sub_537FC0(Args, Str);
                                          }
                                          else
                                          {
                                            return sub_537FA6(Args, Str);
                                          }
                                        }
                                        else
                                        {
                                          return sub_537F8C(Args, Str);
                                        }
                                      }
                                      else
                                      {
                                        return sub_423DB7(Args, Str);
                                      }
                                    }
                                    else
                                    {
                                      return sub_63717A(Args, Str);
                                    }
                                  }
                                  else
                                  {
                                    return CStage::OnPacket(Args, (int)Str);
                                  }
                                }
                                else
                                {
                                  return sub_775FE6(Args, Str);
                                }
                              }
                              else
                              {
                                return sub_79B382(Args, (int)Str);
                              }
                            }
                            else
                            {
                              return sub_756DA7(Args, Str);
                            }
                          }
                          else
                          {
                            return sub_58DE79(Args, Str);
                          }
                        }
                        else
                        {
                          return sub_734FF9(Args, Str);
                        }
                      }
                      else
                      {
                        return sub_7BD6A1(Args, Str);
                      }
                    }
                    else
                    {
                      return sub_431A3E(Args, (char)Str);
                    }
                  }
                  else
                  {
                    return sub_65AC81(Args, Str);
                  }
                }
                else
                {
                  return sub_5058DB(Args, Str);
                }
              }
              else
              {
                return sub_510E50(Args, Str);
              }
            }
            else
            {
              return sub_6D9734(Args, Str);
            }
          }
          else
          {
            return sub_67930E(Args, Str);
          }
        }
        else
        {
          return sub_97208C(Args, Str);
        }
        break;
    }
  }
  else if ( Args == 302 )
  {
    return sub_5335A3((char)Str);
  }
  else
  {
    switch ( Args )
    {
      case 131:
        result = sub_53185C(Str);
        break;
      case 132:
        result = sub_531A08(Str);
        break;
      case 133:
        result = sub_531B7B(Str);
        break;
      case 134:
        result = sub_531E00(Str);
        break;
      case 135:
        result = sub_53228E(Str);
        break;
      case 136:
        result = sub_532087(Str);
        break;
      case 137:
        result = sub_532FCF(Str);
        break;
      case 138:
        result = sub_5330F7((wchar_t *)Str);
        break;
      case 139:
        result = sub_53300B(Str);
        break;
      case 140:
        result = sub_533057(Str);
        break;
      case 141:
        result = sub_5330B6(Str);
        break;
      case 142:
        result = sub_535179(Str);
        break;
      case 143:
        result = sub_535224(Str);
        break;
      case 144:
        result = sub_5352E9((int)Str);
        break;
      case 145:
        result = sub_535A57(Str);
        break;
      case 146:
        result = sub_5360C0(Str);
        break;
      case 147:
        result = (*(int (__thiscall **)(char *, char *))(*((_DWORD *)this - 2) + 44))(this - 8, Str);
        break;
      case 150:
        result = sub_5378BA(Str);
        break;
      case 151:
        result = sub_5378CD(Str);
        break;
      case 152:
        result = sub_5364C5(Str);
        break;
      case 153:
        result = sub_537A1E(Str);
        break;
      case 154:
        result = sub_53184A(Str);
        break;
      case 156:
        result = sub_537A6A(Str);
        break;
      case 159:
        result = sub_72B82A(Str);
        break;
      default:
        goto LABEL_35;
    }
  }
  return result;
}

```

### `CWvsContext::OnPacket` @ `0xa07a08` (1,158B → 284 行)

```c
int __fastcall CWvsContext::OnPacket(void *a1, int a2, int a3, char *Args)
{
  int result; // eax

  // Credits Sunnyboy @ http://forum.ragezone.com/
  result = a3;
  switch ( a3 )
  {
    case 29:
      result = sub_A1EAD9(a1, (int)Args);
      break;
    case 30:
      result = sub_A1F881(Args);
      break;
    case 31:
      result = sub_A1FB52(Args);
      break;
    case 32:
      result = sub_A202BE(Args);
      break;
    case 33:
      result = sub_A2071F(Args);
      break;
    case 34:
      result = sub_A208FF(Args);
      break;
    case 35:
      result = sub_A2091C(Args);
      break;
    case 36:
      result = sub_A1E48C(Args);
      break;
    case 37:
      result = sub_A209B2(Args);
      break;
    case 38:
      result = sub_A223DC((char)Args);
      break;
    case 39:
      result = sub_A209D4((char)Args);
      break;
    case 40:
      result = sub_A20AC0(Args);
      break;
    case 41:
      result = sub_A2508B(Args);
      break;
    case 42:
      result = sub_A25268(Args);
      break;
    case 43:
      result = sub_A265C2((char)Args);
      break;
    case 45:
      result = sub_A27891((char)Args);
      break;
    case 46:
      result = sub_A27B38(Args);
      break;
    case 47:
      result = sub_A27B61(Args);
      break;
    case 48:
      result = sub_A29115(Args);
      break;
    case 49:
      result = sub_A26D44(Args);
      break;
    case 50:
      result = sub_A27D75((char)Args);
      break;
    case 51:
      result = sub_A1E5AF(Args);
      break;
    case 52:
      result = sub_A1E943(Args);
      break;
    case 53:
      result = sub_A1E96D(Args);
      break;
    case 55:
      result = sub_A29739(Args);
      break;
    case 57:
      result = sub_A23D92(Args);
      break;
    case 58:
      result = sub_A23D79(Args);
      break;
    case 59:
      result = sub_A1233F(Args);
      break;
    case 61:
      result = sub_A2370B(Args);
      break;
    case 62:
      result = sub_A3E31C(Args);
      break;
    case 63:
      result = sub_A3F2E8(Args);
      break;
    case 65:
      result = sub_A37490(a1, (int)Args);
      break;
    case 66:
      result = sub_A39F4E(Args);
      break;
    case 67:
      result = sub_A226A6(Args);
      break;
    case 68:
      result = sub_A22785(Args);
      break;
    case 69:
      result = sub_A28298(Args);
      break;
    case 70:
      result = sub_A28C29(Args);
      break;
    case 71:
      result = sub_A29013(Args);
      break;
    case 72:
      result = sub_A29886(Args);
      break;
    case 73:
      result = sub_A299EB(Args);
      break;
    case 74:
      result = sub_A2A083(Args);
      break;
    case 75:
      result = sub_A0831D(Args);
      break;
    case 76:
      result = sub_A29049(Args);
      break;
    case 77:
      result = sub_A1EA17(Args);
      break;
    case 78:
      result = sub_A1EAC0(Args);
      break;
    case 79:
      result = sub_A0800E(Args);
      break;
    case 80:
      result = sub_A08342(Args);
      break;
    case 81:
      result = sub_A0834E(Args);
      break;
    case 82:
      result = sub_A08362(Args);
      break;
    case 83:
      result = sub_A081B8(Args);
      break;
    case 84:
      result = sub_A082D5(Args);
      break;
    case 85:
      result = sub_A082F7(Args);
      break;
    case 86:
      result = sub_A129ED(Args);
      break;
    case 87:
      result = sub_A12A11(Args);
      break;
    case 88:
      result = sub_A12AA0(Args);
      break;
    case 89:
      result = sub_A12B2F(Args);
      break;
    case 90:
      result = sub_A12BD6(Args);
      break;
    case 91:
      result = sub_A12FAC(Args);
      break;
    case 92:
      result = sub_A13081(Args);
      break;
    case 93:
      result = sub_A1365E(Args);
      break;
    case 94:
      result = sub_A34489(Args);
      break;
    case 95:
      result = sub_A3449F(Args);
      break;
    case 96:
      result = sub_A345FB(Args);
      break;
    case 97:
      result = sub_A349AB(Args);
      break;
    case 98:
      result = sub_A34A97(Args);
      break;
    case 99:
      result = sub_A34B8D(Args);
      break;
    case 100:
      result = sub_A34C1B(Args);
      break;
    case 101:
      result = sub_A34DD7(Args);
      break;
    case 102:
      result = sub_A34EDB(Args);
      break;
    case 103:
      result = sub_A34FA4(Args);
      break;
    case 104:
      result = sub_A350C8(Args);
      break;
    case 105:
      result = sub_A13868(Args);
      break;
    case 106:
      result = sub_A139F5(Args);
      break;
    case 107:
      result = sub_A13B20(Args);
      break;
    case 109:
      result = sub_A2A353(Args);
      break;
    case 110:
      result = sub_A2A3BC(Args);
      break;
    case 111:
      result = sub_A2A486(Args);
      break;
    case 112:
      result = sub_A2A65B(Args);
      break;
    case 113:
      result = sub_A2A677(Args);
      break;
    case 114:
      result = sub_A2A82D(Args);
      break;
    case 115:
      result = sub_A2A99D(Args);
      break;
    case 116:
      result = sub_A2AA49(Args);
      break;
    case 117:
      result = sub_A2ACE9(Args);
      break;
    case 118:
      result = sub_A2AD85(Args);
      break;
    case 119:
      result = sub_A2B39A((char)Args);
      break;
    case 120:
      result = sub_A2A7E6((char)a1, (int)Args);
      break;
    case 121:
      result = sub_A13C6C(Args);
      break;
    case 122:
      result = sub_A13F20(Args);
      break;
    case 123:
      result = sub_A13F8D(Args);
      break;
    case 124:
      result = sub_A290F8(Args);
      break;
    default:
      return result;
  }
  return result;
}

```

## String Pool

### `StringPool::GetString` @ `0x406455` (28B → 6 行)

```c
int __stdcall StringPool::GetString(int a1, int a2)
{
  sub_79E993(a1, a2, 0);
  return a1;
}

```

## Network Encode/Decode

## Entry Point

### `_WinMain@16` @ `0x9f19f2` (2,798B → 134 行)

```c
int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
  const char *v4; // eax
  int v5; // eax
  size_t v6; // eax
  int v7; // ecx
  HWND v8; // ecx
  int v9; // eax
  bool v10; // zf
  int v11; // ecx
  HWND v12; // ecx
  HWND v14; // [esp-94h] [ebp-608h] BYREF
  int v15; // [esp-90h] [ebp-604h] BYREF
  int v16; // [esp-8Ch] [ebp-600h]
  HWND v17; // [esp-5Ch] [ebp-5D0h] BYREF
  int v18; // [esp-58h] [ebp-5CCh] BYREF
  int v19; // [esp-54h] [ebp-5C8h]
  int v20; // [esp-4h] [ebp-578h]
  int v21; // [esp+0h] [ebp-574h] BYREF
  _BYTE Str[260]; // [esp+10h] [ebp-564h] BYREF
  _DWORD Dst[17]; // [esp+428h] [ebp-14Ch] BYREF
  _BYTE v24[16]; // [esp+46Ch] [ebp-108h] BYREF
  _BYTE v25[28]; // [esp+47Ch] [ebp-F8h] BYREF
  HWND *v26; // [esp+4A8h] [ebp-CCh]
  int v27; // [esp+4ACh] [ebp-C8h]
  HWND *v28; // [esp+53Ch] [ebp-38h]
  int v29; // [esp+550h] [ebp-24h]
  int v30; // [esp+554h] [ebp-20h] BYREF
  HWND *v31; // [esp+55Ch] [ebp-18h] BYREF
  int v32[2]; // [esp+560h] [ebp-14h] BYREF
  int v33; // [esp+570h] [ebp-4h]
  int Src; // [esp+57Ch] [ebp+8h]

  v32[1] = (int)&v21;
  dword_BF1670 = (int)hInstance;
  v4 = (const char *)sub_9F9808();
  if ( v4 )
    strcpy(Dest, v4);
  dword_BF0910 = 0;
  dword_BF091C = (int)sub_9F9893;
  dword_BF0914 = 1;
  dword_BF0918 = 1;
  StringPool::GetInstance();
  v20 = *(_DWORD *)StringPool::GetString((int)&v31, 945);
  v33 = 0;
  v5 = dword_BF02E8(0, 1, v20);
  v33 = -1;
  Src = v5;
  sub_4062DF(&v31);
  if ( Src )
  {
    dword_BF03A4();
    sub_9F17E9();
    dword_BF0394(260, Str);
    v30 = 0;
    sub_414617(Str, 0xFFFFFFFF);
    v33 = 3;
    v6 = strlen("\\npkgameuninstnomsg.exe");
    sub_428D30("\\npkgameuninstnomsg.exe", v6);
    memset(Dst, 0, sizeof(Dst));
    Dst[0] = 68;
    dword_BF02AC(v30, 0, 0, 0, 0, 32, 0, 0, Dst, v24);
    if ( dword_BF056C(0) >= 0 )
    {
      v33 = 3;
      v31 = 0;
      v29 = 0;
      v9 = sub_403065(1072);
      LOBYTE(v33) = 8;
      if ( v9 )
        sub_49C213(v9);
      LOBYTE(v33) = 10;
      sub_9F4FDA(v25, lpCmdLine);
      LOBYTE(v33) = 11;
      sub_9F5239(v25);
      LOBYTE(v33) = 12;
      lpCmdLine = 0;
      sub_9F5C50(v25, &lpCmdLine);
      v31 = v26;
      if ( !v27 || (v10 = *(_DWORD *)(dword_BEBF9C + 20) == 0, v29 = 1, v10) )
        v29 = 0;
      LOBYTE(v33) = 10;
      sub_9F51F6(v25);
      LOBYTE(v33) = 9;
      sub_9F24E0(v32);
      v33 = 3;
      sub_9F17E9();
      if ( v29 )
      {
        sub_98EB77();
        v16 = 0;
        sub_414617((void *)&Str2, 0xFFFFFFFF);
        v15 = v11;
        lpCmdLine = (LPSTR)&v15;
        LOBYTE(v33) = 59;
        sub_428DB3((void *)&Str2, 0xFFFFFFFF);
        v14 = v12;
        v28 = &v14;
        LOBYTE(v33) = 60;
        StringPool::GetInstance();
        StringPool::GetString((int)&v14, 920);
        LOBYTE(v33) = 3;
        sub_68DCC2(v14, v15, v16);
      }
      if ( dword_BEC3A8 )
        sub_9F2601();
      sub_987A6A("MapleStoryGlobal :: MapleStory - Microsoft Internet Explorer");
      if ( dword_BEBF9C )
        (**(void (__thiscall ***)(int, int))dword_BEBF9C)(dword_BEBF9C, 1);
      dword_BF0568();
    }
    else
    {
      sub_98EB77();
      v19 = 0;
      sub_414617((void *)&Str2, 0xFFFFFFFF);
      v18 = v7;
      lpCmdLine = (LPSTR)&v18;
      LOBYTE(v33) = 4;
      sub_428DB3((void *)&Str2, 0xFFFFFFFF);
      v17 = v8;
      v31 = &v17;
      LOBYTE(v33) = 5;
      StringPool::GetInstance();
      StringPool::GetString((int)&v17, 2551);
      LOBYTE(v33) = 3;
      sub_68DCC2(v17, v18, v19);
    }
    v33 = -1;
    sub_4062DF(&v30);
  }
  return 0;
}

```
