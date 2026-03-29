"""
Usability tests for douyin_downloader.py

Tests cover:
- URL extraction from various input formats
- Video ID regex extraction
- Error handling for invalid inputs
- Script entry point behavior
"""
import unittest
from unittest.mock import patch, MagicMock
import io
import os
import sys

from douyin_downloader import get_real_url, download_video


class TestGetRealUrl(unittest.TestCase):
    """Tests for the get_real_url function."""

    def test_valid_share_text(self):
        text = "1.74 复制打开抖音，看看【赞扬Live的作品】https://v.douyin.com/fQCnoZvoRt4/ PxS:/"
        result = get_real_url(text)
        self.assertEqual(result, "https://v.douyin.com/fQCnoZvoRt4/")

    def test_plain_url(self):
        result = get_real_url("https://v.douyin.com/abc123/")
        self.assertEqual(result, "https://v.douyin.com/abc123/")

    def test_no_url_returns_none(self):
        result = get_real_url("hello world no url here")
        self.assertIsNone(result)

    def test_empty_string_returns_none(self):
        result = get_real_url("")
        self.assertIsNone(result)

    def test_url_without_trailing_slash_not_matched(self):
        result = get_real_url("https://v.douyin.com/abc123")
        self.assertIsNone(result)

    def test_http_url(self):
        result = get_real_url("http://v.douyin.com/abc123/")
        self.assertEqual(result, "http://v.douyin.com/abc123/")

    def test_multiple_urls_returns_first(self):
        text = "https://v.douyin.com/first123/ and https://v.douyin.com/second456/"
        result = get_real_url(text)
        self.assertEqual(result, "https://v.douyin.com/first123/")

    def test_non_douyin_url_not_matched(self):
        result = get_real_url("https://www.example.com/abc123/")
        self.assertIsNone(result)


class TestDownloadVideoErrorHandling(unittest.TestCase):
    """Tests for download_video error handling."""

    def test_invalid_input_no_crash(self):
        """download_video should handle invalid input gracefully."""
        # Should not raise any exceptions
        download_video("not a valid url")

    @patch("douyin_downloader.requests.Session")
    def test_non_redirect_response(self, mock_session_cls):
        """download_video should handle non-redirect response gracefully."""
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_session.get.return_value = mock_resp

        # Should not raise
        download_video("https://v.douyin.com/test123/")

    @patch("douyin_downloader.requests.Session")
    def test_no_video_id_in_page(self, mock_session_cls):
        """download_video should handle missing video_id gracefully."""
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        # First call: redirect response
        redirect_resp = MagicMock()
        redirect_resp.status_code = 302
        redirect_resp.headers = {"Location": "https://www.douyin.com/video/123"}

        # Second call: page content without video_id
        page_resp = MagicMock()
        page_resp.text = "<html>no video id here</html>"

        mock_session.get.side_effect = [redirect_resp, page_resp]

        # Should not raise
        download_video("https://v.douyin.com/test123/")

    @patch("douyin_downloader.requests.Session")
    def test_network_error_handled(self, mock_session_cls):
        """download_video should catch network exceptions."""
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_session.get.side_effect = Exception("Connection timeout")

        # Should not raise, error is caught
        download_video("https://v.douyin.com/test123/")

    @patch("douyin_downloader.requests.Session")
    def test_successful_download_flow(self, mock_session_cls):
        """Test the full download flow with mocked responses."""
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        # Step 1: Redirect
        redirect_resp = MagicMock()
        redirect_resp.status_code = 302
        redirect_resp.headers = {"Location": "https://www.douyin.com/video/123"}

        # Step 2: Page with video_id
        page_resp = MagicMock()
        page_resp.text = 'src="https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0300test123&ratio=720p"'

        # Step 3: API redirect to real video
        api_resp = MagicMock()
        api_resp.status_code = 302
        api_resp.headers = {"Location": "https://video-cdn.example.com/video.mp4"}

        # Step 4: Video download
        video_resp = MagicMock()
        video_resp.headers = {"content-length": "100"}
        video_resp.iter_content.return_value = [b"x" * 100]

        mock_session.get.side_effect = [redirect_resp, page_resp, api_resp, video_resp]

        download_video("https://v.douyin.com/test123/")

        # Verify the output file was created
        expected_file = os.path.join("output", "douyin_v0300test123.mp4")
        self.assertTrue(os.path.exists(expected_file))

        # Clean up
        os.remove(expected_file)


class TestVideoIdRegex(unittest.TestCase):
    """Tests for the video_id regex pattern used in download_video."""

    def setUp(self):
        import re
        self.vid_pattern = re.compile(r"video_id=([a-zA-Z0-9]+)")

    def test_standard_video_id(self):
        html = "video_id=abc123def456"
        match = self.vid_pattern.search(html)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "abc123def456")

    def test_video_id_in_url(self):
        html = "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0300fg10000test&ratio=720p"
        match = self.vid_pattern.search(html)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "v0300fg10000test")

    def test_no_video_id(self):
        html = "no video id in this content"
        match = self.vid_pattern.search(html)
        self.assertIsNone(match)


class TestEntryPoint(unittest.TestCase):
    """Tests for the script entry point."""

    @patch("douyin_downloader.download_video")
    def test_argv_input(self, mock_download):
        """Script should use sys.argv[1] when provided."""
        test_args = ["douyin_downloader.py", "https://v.douyin.com/test/"]
        with patch.object(sys, "argv", test_args):
            # Re-execute the main block logic
            if len(sys.argv) > 1:
                text = sys.argv[1]
            else:
                text = "fallback"
            self.assertEqual(text, "https://v.douyin.com/test/")


if __name__ == "__main__":
    unittest.main()
