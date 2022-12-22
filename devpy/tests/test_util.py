import mock
import pytest
import subprocess
import sys

import devpy.cmds.util as util


def run_devpy(extra_args):
    p = subprocess.run(
        [sys.executable, "-m", "devpy"] + extra_args, capture_output=True
    )
    if p.returncode != 0:
        print(p.stdout.decode("utf-8"), end="")
        print(p.stderr.decode("utf-8"), end="")
        raise RuntimeError("Failed to execute dev.py; see printed stdout/stderr")
    return p


def test_get_site_packages_window():
    with mock.patch("os.walk") as mockwalk:
        mockwalk.return_value = [
            ("meson-install/Lib", ("bar", "site-packages"), ("test",)),
            ("meson-install/Lib", ("bar", "not-site-packages"), ("test",)),
        ]
        res = util.get_site_packages("meson-install")
        assert "/meson-install/Lib/site-packages" in res


def test_get_site_packages_linux():
    pymm = f"python{sys.version_info.major}.{sys.version_info.minor}"
    expected = f"meson-install/lib/{pymm}"
    other = "meson-install/lib/python2.15"
    with mock.patch("os.walk") as mockwalk:
        mockwalk.return_value = [
            (expected, ("bar", "site-packages"), ("test",)),
            (other, ("bar", "site-packages"), ("test",)),
        ]
        res = util.get_site_packages("meson-install")
        assert expected in res


def test_get_site_packages_fail():
    expected = "meson-install/lib"
    with mock.patch("os.walk") as mockwalk:
        mockwalk.return_value = [
            (expected, ("bar", "site-packages"), ("test",)),
            (expected, ("foo", "site-packages"), ("test",)),
        ]
        with pytest.raises(ValueError):
            res = util.get_site_packages("meson-install")
            print(res)
