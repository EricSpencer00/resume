import tempfile
import unittest
from pathlib import Path

from scripts.sync_pdfs import SyncError, sync_pdfs


class SyncPdfsTests(unittest.TestCase):
    def test_replaces_stale_pdfs_and_preserves_non_pdf_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "out"
            destination = root / "site" / "assets" / "pdf"
            source.mkdir()
            destination.mkdir(parents=True)

            (source / "cv.pdf").write_bytes(b"new cv")
            (source / "resume-81326.pdf").write_bytes(b"new resume")
            (source / "build.log").write_text("ignored", encoding="utf-8")
            (destination / "cv.pdf").write_bytes(b"old cv")
            (destination / "resume-81326.pdf").write_bytes(b"old resume")
            (destination / "resume-retired.pdf").write_bytes(b"stale")
            (destination / "keep.txt").write_text("site metadata", encoding="utf-8")

            names = sync_pdfs(source, destination)

            self.assertEqual(names, ["cv.pdf", "resume-81326.pdf"])
            self.assertEqual(
                sorted(path.name for path in destination.iterdir()),
                ["cv.pdf", "keep.txt", "resume-81326.pdf"],
            )
            self.assertEqual((destination / "cv.pdf").read_bytes(), b"new cv")
            self.assertEqual(
                (destination / "resume-81326.pdf").read_bytes(), b"new resume"
            )

    def test_invalid_build_output_does_not_mutate_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "out"
            destination = root / "site" / "assets" / "pdf"
            source.mkdir()
            destination.mkdir(parents=True)
            stale = destination / "resume-retired.pdf"
            stale.write_bytes(b"stale")

            with self.assertRaises(SyncError):
                sync_pdfs(source, destination)

            self.assertEqual(stale.read_bytes(), b"stale")
            self.assertEqual(sorted(path.name for path in destination.iterdir()), [stale.name])

    def test_unexpected_pdf_is_rejected_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "out"
            destination = root / "site" / "assets" / "pdf"
            source.mkdir()
            destination.mkdir(parents=True)
            stale = destination / "resume-retired.pdf"
            stale.write_bytes(b"stale")
            (source / "cv.pdf").write_bytes(b"cv")
            (source / "resume-81326.pdf").write_bytes(b"resume")
            (source / "unexpected.pdf").write_bytes(b"unexpected")

            with self.assertRaises(SyncError):
                sync_pdfs(source, destination)

            self.assertEqual(stale.read_bytes(), b"stale")
            self.assertEqual(sorted(path.name for path in destination.iterdir()), [stale.name])


if __name__ == "__main__":
    unittest.main()
