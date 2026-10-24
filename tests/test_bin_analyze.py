import os
import struct
import tempfile
import unittest
import zipfile

from _load import load

bin_analyze = load("replica-recon", "bin_analyze")


def write(name, data):
    d = tempfile.mkdtemp()
    p = os.path.join(d, name)
    with open(p, "wb") as fh:
        fh.write(data)
    return p


def pe(machine, managed=False):
    blob = bytearray(0x200)
    blob[0:2] = b"MZ"
    struct.pack_into("<I", blob, 0x3C, 0x80)
    blob[0x80:0x84] = b"PE\x00\x00"
    struct.pack_into("<H", blob, 0x84, machine)
    if managed:
        blob.extend(b"mscoree.dll\x00")
    return bytes(blob)


def elf(machine):
    blob = bytearray(64)
    blob[0:4] = b"\x7fELF"
    blob[4] = 2
    blob[5] = 1
    struct.pack_into("<H", blob, 18, machine)
    return bytes(blob)


def macho(cpu):
    blob = bytearray(32)
    struct.pack_into("<I", blob, 0, 0xCFFAEDFE)
    struct.pack_into("<I", blob, 4, cpu)
    return bytes(blob)


class BinAnalyze(unittest.TestCase):
    def test_pe_native_x64(self):
        self.assertEqual(bin_analyze.detect(write("a.exe", pe(0x8664)))["format"],
                         "pe-native")
        self.assertEqual(bin_analyze.detect(write("b.exe", pe(0x8664)))["arch"], "x64")

    def test_pe_managed(self):
        info = bin_analyze.detect(write("c.dll", pe(0x014C, managed=True)))
        self.assertEqual(info["format"], "pe-managed")
        self.assertTrue(info["managed"])

    def test_elf_x64(self):
        info = bin_analyze.detect(write("a.elf", elf(0x3E)))
        self.assertEqual(info["format"], "elf")
        self.assertEqual(info["arch"], "x64")

    def test_macho_arm64(self):
        info = bin_analyze.detect(write("a.dylib", macho(0x0100000C)))
        self.assertEqual(info["format"], "mach-o")
        self.assertEqual(info["arch"], "arm64")

    def test_dex(self):
        info = bin_analyze.detect(write("classes.dex", b"dex\n037" + b"\x00" * 32))
        self.assertEqual(info["format"], "dex")
        self.assertEqual(info["version"], "037")

    def test_java_class(self):
        data = b"\xca\xfe\xba\xbe\x00\x00\x00\x34" + b"\x00" * 16
        info = bin_analyze.detect(write("Foo.class", data))
        self.assertEqual(info["format"], "class")

    def test_pyc(self):
        info = bin_analyze.detect(write("mod.pyc", struct.pack("<I", 3531) + b"\x00" * 16))
        self.assertEqual(info["format"], "pyc")
        self.assertEqual(info["version"], "3.12")

    def test_apk(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "app.apk")
        with zipfile.ZipFile(p, "w") as zf:
            zf.writestr("AndroidManifest.xml", "<manifest/>")
            zf.writestr("classes.dex", "dex")
        self.assertEqual(bin_analyze.detect(p)["format"], "apk")

    def test_jar(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "lib.jar")
        with zipfile.ZipFile(p, "w") as zf:
            zf.writestr("META-INF/MANIFEST.MF", "Manifest-Version: 1.0")
            zf.writestr("com/Foo.class", "class")
        self.assertEqual(bin_analyze.detect(p)["format"], "jar")

    def test_asar(self):
        hdr = b'{"files":{}}'
        data = struct.pack("<I", len(hdr)) + hdr
        self.assertEqual(bin_analyze.detect(write("app.asar", data))["format"], "asar")

    def test_go(self):
        data = elf(0x3E) + b"Go build ID: abcdef"
        info = bin_analyze.detect(write("a.bin", data))
        self.assertEqual(info["format"], "elf")
        self.assertEqual(info["runtime"], "go")

    def test_flutter_aot(self):
        data = elf(0x3E) + b"\xdc\xdc\xf5\xf5\xdc\xdc\xf5\xf5"
        info = bin_analyze.detect(write("libapp.so", data))
        self.assertEqual(info["format"], "elf")
        self.assertEqual(info["runtime"], "flutter")

    def test_il2cpp(self):
        data = pe(0x8664) + b"global-metadata.dat"
        info = bin_analyze.detect(write("GameAssembly.dll", data))
        self.assertEqual(info["format"], "pe-native")
        self.assertEqual(info["runtime"], "il2cpp")

    def test_unknown(self):
        info = bin_analyze.detect(write("notes.txt", b"hello world, not a binary"))
        self.assertEqual(info["format"], "unknown")

    def test_upx_packed(self):
        data = pe(0x8664) + b"UPX! packed section"
        info = bin_analyze.detect(write("a.exe", data))
        self.assertEqual(info["format"], "pe-native")
        self.assertEqual(info["protection"][0]["name"], "upx")

    def test_net_obfuscated(self):
        data = pe(0x014C, managed=True) + b"ConfuserEx obfuscated"
        info = bin_analyze.detect(write("a.dll", data))
        names = [p["name"] for p in info["protection"]]
        self.assertIn("confuserex", names)

    def test_analyze_writes_sha256_and_tools(self):
        p = write("app.apk", b"\x00")
        out = tempfile.mkdtemp()
        info = bin_analyze.analyze(p, out)
        self.assertEqual(len(info["sha256"]), 64)
        self.assertIn("tools", info)


if __name__ == "__main__":
    unittest.main()
