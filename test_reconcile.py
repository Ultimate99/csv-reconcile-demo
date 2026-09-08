import tempfile
import unittest
from pathlib import Path
from reconcile import compare


class ReconcileTests(unittest.TestCase):
    def run_compare(self, left, right):
        with tempfile.TemporaryDirectory() as folder:
            a, b = Path(folder) / "a.csv", Path(folder) / "b.csv"
            a.write_text(left, encoding="utf-8")
            b.write_text(right, encoding="utf-8")
            return compare(a, b, "id")

    def test_all_outcomes_and_leading_zeros(self):
        report = self.run_compare("id,value\n001,10\n002,20\n003,30\n", "value,id\n10,001\n25,002\n40,004\n")
        self.assertEqual(report["summary"], {"left_rows": 3, "right_rows": 3, "matched": 1, "differences": 3})
        self.assertEqual([r["status"] for r in report["changes"]], ["changed", "left_only", "right_only"])
        self.assertEqual(report["changes"][0]["fields"]["value"], {"left": "20", "right": "25"})

    def test_bom_unicode_and_quoted_multiline(self):
        data = '\ufeffid,value\n1,"Čaj,\ncoffee"\n'
        self.assertEqual(self.run_compare(data, data)["summary"]["matched"], 1)

    def test_invalid_input_rejected(self):
        for data in ["id,value\n1,a\n1,b\n", "id,value\n,a\n", "id,value\n1\n", "id,value\n1,a,b\n", "id,id\n1,2\n", "id,\n1,a\n", "", "other,value\n1,a\n"]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.run_compare(data, "id,value\n1,a\n")

    def test_schema_mismatch(self):
        with self.assertRaises(ValueError):
            self.run_compare("id,a\n1,x\n", "id,b\n1,x\n")


if __name__ == "__main__":
    unittest.main()
