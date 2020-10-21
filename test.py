import configparser
import unittest
from parser import parse_url

disable_resource_warnings = 1


config = configparser.ConfigParser()
config.read("config")
github_token = config["settings"]["github_token"]


test_urls = {
    "https://github.com/bitcoin-core-review-club/bitcoin/blob/master/src/addrman.cpp#L18": "src/addrman.cpp#L18",
    "https://github.com/bitcoin-core-review-club/bitcoin/blob/master/src/addrman.cpp": "src/addrman.cpp",
    "https://github.com/bitcoin-core-review-club/bitcoin/commit/805a79abea841f8da6c219f7e649f7084c8b6386#diff-a0337ffd7259e8c7c9a7786d6dbd420c80abfa1afdb34ebae3261109d9ae3c19R395": "src/script/interpreter.cpp#L395",
    "https://github.com/bitcoin-core-review-club/bitcoin/commit/805a79abea841f8da6c219f7e649f7084c8b6386#diff-a0337ffd7259e8c7c9a7786d6dbd420c80abfa1afdb34ebae3261109d9ae3c19": "src/script/interpreter.cpp",
    "https://github.com/bitcoin-core-review-club/bitcoin/commit/805a79abea841f8da6c219f7e649f7084c8b6386": "commit: 805a79abea841f8da6c219f7e649f7084c8b6386",
    "https://github.com/bitcoin-core-review-club/bitcoin/commit/805a79abea841f8da6c219f7e649f7084c8b6386?branch=805a79abea841f8da6c219f7e649f7084c8b6386&diff=unified#diff-b4a26abc33ab9360dda8185fbfe5a2335e8bd4ea55172d4bf1ec81056973f8dbR61": "src/script/script_error.h#L61",
    "https://github.com/bitcoin/bitcoin/commit/c56c9ad7210751de862f0d0122579b626db01fe4#diff-ac18f9768d83fd8236527f3aebc335b1a3d971321ba15d2c24852879d6f87e5fR9": "doc/man/bitcoin-qt.1#L9",
    "https://github.com/bitcoin/bitcoin/blob/0.17/contrib/windeploy/win-codesign.cert#L28": "contrib/windeploy/win-codesign.cert#L28",
    "https://www.google.com": "",
    "https://github.com/bitcoin/bitcoin/pull/20145/commits/355d0c4f6b8a7687a3940a2d90d66b08e560bfa7#diff-6612de31c2bd73d12f71d485cb5d0e6fedf4141facfba3479fa0bce318da86b0R6": "contrib/signet/getcoins.py#L6",
    "https://github.com/bitcoin/bitcoin/pull/19055/files#diff-ccad840af4d1bda6dda986297fdd142a8cf433cd4ab4222eea20fe1fd229a158R16": "src/crypto/muhash.cpp#L16",
}


class TestParser(unittest.TestCase):
    def setUp(self):
        if disable_resource_warnings:
            import warnings

            warnings.simplefilter("ignore")

    def test_urls(self):
        for url, result in test_urls.items():
            print(f"url: {url}, result: {result}")
            ref = parse_url(url, github_token)
            self.assertEqual(ref, result)


if __name__ == "__main__":
    unittest.main()
