#!/usr/bin/env python3
"""Decode Android's binary XML (AXML) to a readable XML string.

This is a small, self-contained decoder (no external deps).
Supports typical AndroidManifest.xml and layout XML.

Based on the AXML chunk format as used by Android resources.
"""

import io
import struct
import sys
from typing import List, Tuple, Optional

# Chunk types
RES_STRING_POOL_TYPE = 0x0001
RES_XML_TYPE = 0x0003
RES_XML_START_NAMESPACE_TYPE = 0x0100
RES_XML_END_NAMESPACE_TYPE = 0x0101
RES_XML_START_ELEMENT_TYPE = 0x0102
RES_XML_END_ELEMENT_TYPE = 0x0103
RES_XML_CDATA_TYPE = 0x0104
RES_XML_RESOURCE_MAP_TYPE = 0x0180

# Value types (TypedValue)
TYPE_NULL = 0x00
TYPE_REFERENCE = 0x01
TYPE_ATTRIBUTE = 0x02
TYPE_STRING = 0x03
TYPE_FLOAT = 0x04
TYPE_DIMENSION = 0x05
TYPE_FRACTION = 0x06
TYPE_FIRST_INT = 0x10
TYPE_INT_DEC = 0x10
TYPE_INT_HEX = 0x11
TYPE_INT_BOOLEAN = 0x12
TYPE_FIRST_COLOR_INT = 0x1c
TYPE_INT_COLOR_ARGB8 = 0x1c
TYPE_INT_COLOR_RGB8 = 0x1d
TYPE_INT_COLOR_ARGB4 = 0x1e
TYPE_INT_COLOR_RGB4 = 0x1f

RADIX_MULTS = [
    1.0 / (1 << 23),
    1.0 / (1 << 15),
    1.0 / (1 << 7),
    1.0,
]
DIMENSION_UNITS = ["px", "dp", "sp", "pt", "in", "mm", "??", "??"]
FRACTION_UNITS = ["%", "%p", "??", "??", "??", "??", "??", "??"]


def u16(buf: bytes, off: int) -> int:
    return struct.unpack_from('<H', buf, off)[0]


def u32(buf: bytes, off: int) -> int:
    return struct.unpack_from('<I', buf, off)[0]


def s32(buf: bytes, off: int) -> int:
    return struct.unpack_from('<i', buf, off)[0]


class StringPool:
    def __init__(self, strings: List[str]):
        self.strings = strings

    def get(self, idx: int) -> str:
        if idx is None or idx < 0 or idx >= len(self.strings):
            return ""
        return self.strings[idx]


def read_chunk_header(fp: io.BufferedReader) -> Tuple[int, int, int]:
    data = fp.read(8)
    if len(data) < 8:
        raise EOFError
    ctype, header_size, size = struct.unpack('<HHI', data)
    return ctype, header_size, size


def parse_string_pool(fp: io.BufferedReader, chunk_size: int, header_size: int) -> StringPool:
    # Header already partially read (8 bytes). We need remaining header bytes.
    remaining = header_size - 8
    hdr = fp.read(remaining)
    if len(hdr) != remaining:
        raise ValueError("Truncated string pool header")

    string_count, style_count, flags, strings_start, styles_start = struct.unpack('<IIIII', hdr[:20])
    is_utf8 = (flags & 0x00000100) != 0

    # Offsets arrays
    string_offsets = [u32(fp.read(4), 0) for _ in range(string_count)]
    # Skip style offsets
    fp.read(4 * style_count)

    # Now read the entire strings+styles data in this chunk
    data_size = chunk_size - header_size - 4 * string_count - 4 * style_count
    data = fp.read(data_size)
    if len(data) != data_size:
        raise ValueError("Truncated string pool data")

    def read_utf8(off: int) -> str:
        # UTF-8 strings store two lengths (utf16_len, utf8_len), both in a special format.
        def read_len(o: int) -> Tuple[int, int]:
            first = data[o]
            if first & 0x80:
                second = data[o+1]
                val = ((first & 0x7f) << 7) | (second & 0x7f)
                return val, 2
            return first, 1

        o = off
        _, adv1 = read_len(o)
        o += adv1
        utf8_len, adv2 = read_len(o)
        o += adv2
        s = data[o:o+utf8_len]
        return s.decode('utf-8', errors='replace')

    def read_utf16(off: int) -> str:
        o = off
        # length in utf16 code units, stored as u16 or two u16.
        l = u16(data, o)
        o += 2
        if l & 0x8000:
            l2 = u16(data, o)
            o += 2
            l = ((l & 0x7fff) << 16) | l2
        byte_len = l * 2
        s = data[o:o+byte_len]
        return s.decode('utf-16le', errors='replace')

    strings: List[str] = []
    for so in string_offsets:
        if is_utf8:
            strings.append(read_utf8(so))
        else:
            strings.append(read_utf16(so))

    return StringPool(strings)


def complex_to_float(x: int) -> float:
    mantissa = x & 0xFFFFFF00
    radix = (x >> 4) & 0x3
    return mantissa * RADIX_MULTS[radix]


def format_typed_value(vtype: int, data: int, sp: StringPool) -> str:
    if vtype == TYPE_STRING:
        return sp.get(data)
    if vtype == TYPE_ATTRIBUTE:
        return f"?0x{data:08x}"
    if vtype == TYPE_REFERENCE:
        return f"@0x{data:08x}"
    if vtype == TYPE_FLOAT:
        return str(struct.unpack('<f', struct.pack('<I', data))[0])
    if vtype == TYPE_INT_HEX:
        return f"0x{data:08x}"
    if vtype == TYPE_INT_BOOLEAN:
        return "true" if data != 0 else "false"
    if vtype == TYPE_DIMENSION:
        unit = DIMENSION_UNITS[data & 0xF]
        return f"{complex_to_float(data):g}{unit}"
    if vtype == TYPE_FRACTION:
        unit = FRACTION_UNITS[data & 0xF]
        return f"{complex_to_float(data)*100:g}{unit}"
    if TYPE_FIRST_COLOR_INT <= vtype <= TYPE_INT_COLOR_RGB4:
        return f"#{data:08x}"
    if TYPE_FIRST_INT <= vtype <= TYPE_INT_BOOLEAN:
        return str(struct.unpack('<i', struct.pack('<I', data))[0])
    if vtype == TYPE_NULL:
        return ""
    return f"(type 0x{vtype:02x}) 0x{data:08x}"


def decode_axml(path: str) -> str:
    with open(path, 'rb') as f:
        fp = io.BufferedReader(f)

        # First chunk header should be RES_XML_TYPE
        ctype, header_size, size = read_chunk_header(fp)
        if ctype != RES_XML_TYPE:
            raise ValueError(f"Not an XML resource (type=0x{ctype:04x})")
        # Skip remaining header bytes (usually 8, already read)
        fp.read(header_size - 8)

        string_pool: Optional[StringPool] = None
        resource_map: List[int] = []
        ns_stack: List[Tuple[str, str]] = []  # prefix, uri
        indent = 0
        out: List[str] = []

        # Read chunks until EOF
        while True:
            try:
                ctype, hsize, csize = read_chunk_header(fp)
            except EOFError:
                break

            chunk_start = fp.tell() - 8

            if ctype == RES_STRING_POOL_TYPE:
                string_pool = parse_string_pool(fp, csize, hsize)
            elif ctype == RES_XML_RESOURCE_MAP_TYPE:
                # map of resource ids used by attributes (optional)
                count = (csize - hsize) // 4
                # ResXMLTree_node header is 16 bytes (incl. lineNumber+comment).
                # We have already consumed 8 bytes of the chunk header, so read the
                # remaining (hsize-8) bytes for the node header.
                fp.read(max(0, hsize - 8))
                resource_map = [u32(fp.read(4), 0) for _ in range(count)]
            elif ctype in (RES_XML_START_NAMESPACE_TYPE, RES_XML_END_NAMESPACE_TYPE):
                # ResXMLTree_node: lineNumber + comment follow immediately after the
                # chunk header. Do not skip them.
                line_no = u32(fp.read(4), 0)
                _comment = u32(fp.read(4), 0)
                prefix_idx = s32(fp.read(4), 0)
                uri_idx = s32(fp.read(4), 0)
                if not string_pool:
                    raise ValueError("String pool not parsed")
                prefix = string_pool.get(prefix_idx)
                uri = string_pool.get(uri_idx)
                if ctype == RES_XML_START_NAMESPACE_TYPE:
                    ns_stack.append((prefix, uri))
                else:
                    if ns_stack:
                        ns_stack.pop()
            elif ctype == RES_XML_START_ELEMENT_TYPE:
                if not string_pool:
                    raise ValueError("String pool not parsed")
                _line_no = u32(fp.read(4), 0)
                _comment = u32(fp.read(4), 0)
                ns_idx = s32(fp.read(4), 0)
                name_idx = s32(fp.read(4), 0)
                _attr_start = u16(fp.read(2), 0)
                _attr_size = u16(fp.read(2), 0)
                attr_count = u16(fp.read(2), 0)
                _id_index = u16(fp.read(2), 0)
                _class_index = u16(fp.read(2), 0)
                _style_index = u16(fp.read(2), 0)

                ns_uri = string_pool.get(ns_idx) if ns_idx != -1 else ""
                name = string_pool.get(name_idx)

                # Collect attributes
                attrs = []
                for _ in range(attr_count):
                    a_ns = s32(fp.read(4), 0)
                    a_name = s32(fp.read(4), 0)
                    a_raw = s32(fp.read(4), 0)
                    # Res_value (TypedValue): size (u16), res0 (u8), dataType (u8), data (u32)
                    _size = u16(fp.read(2), 0)
                    _res0 = fp.read(1)  # unused
                    vtype = fp.read(1)[0]
                    vdata = u32(fp.read(4), 0)

                    a_ns_uri = string_pool.get(a_ns) if a_ns != -1 else ""
                    a_name_s = string_pool.get(a_name)
                    raw_s = string_pool.get(a_raw) if a_raw != -1 else None
                    val_s = raw_s if raw_s is not None else format_typed_value(vtype, vdata, string_pool)

                    attrs.append((a_ns_uri, a_name_s, val_s))

                # Element open
                ind = "  " * indent
                # Namespace prefix mapping for printing
                ns_decl = ""
                if indent == 0 and ns_stack:
                    # declare all namespaces seen so far
                    parts = []
                    for p, u in ns_stack:
                        if p:
                            parts.append(f'xmlns:{p}="{u}"')
                        else:
                            parts.append(f'xmlns="{u}"')
                    ns_decl = (" " + " ".join(parts)) if parts else ""

                # Attribute rendering with android: prefix when possible
                def prefix_for_uri(uri: str) -> str:
                    for p, u in reversed(ns_stack):
                        if u == uri:
                            return p
                    return ""

                attr_txt = []
                for a_uri, a_name_s, a_val in attrs:
                    p = prefix_for_uri(a_uri)
                    if p:
                        attr_txt.append(f'{p}:{a_name_s}="{a_val}"')
                    else:
                        attr_txt.append(f'{a_name_s}="{a_val}"')

                if attr_txt:
                    out.append(f"{ind}<{name}{ns_decl} " + " ".join(attr_txt) + ">")
                else:
                    out.append(f"{ind}<{name}{ns_decl}>")

                indent += 1
            elif ctype == RES_XML_END_ELEMENT_TYPE:
                if not string_pool:
                    raise ValueError("String pool not parsed")
                _line_no = u32(fp.read(4), 0)
                _comment = u32(fp.read(4), 0)
                _ns_idx = s32(fp.read(4), 0)
                name_idx = s32(fp.read(4), 0)
                name = string_pool.get(name_idx)
                indent = max(0, indent - 1)
                ind = "  " * indent
                out.append(f"{ind}</{name}>")
            elif ctype == RES_XML_CDATA_TYPE:
                if not string_pool:
                    raise ValueError("String pool not parsed")
                _line_no = u32(fp.read(4), 0)
                _comment = u32(fp.read(4), 0)
                data_idx = s32(fp.read(4), 0)
                _size = u16(fp.read(2), 0)
                _res0 = fp.read(1)
                vtype = fp.read(1)[0]
                vdata = u32(fp.read(4), 0)
                text = string_pool.get(data_idx)
                ind = "  " * indent
                out.append(f"{ind}{text}")
            else:
                # Skip unknown chunk
                fp.seek(chunk_start + csize)

        return "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" + "\n".join(out) + "\n"


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <AndroidManifest.xml|layout.xml>", file=sys.stderr)
        sys.exit(2)
    print(decode_axml(sys.argv[1]), end="")


if __name__ == "__main__":
    main()
