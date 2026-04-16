#!/usr/bin/env python3
"""
LinkedIn C++ Q&A Auto Poster
Posts C++ questions daily at 9 PM JST - answers handled manually
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, List

# Import LinkedIn API
try:
    from linkedin_api_v2 import LinkedInPoster
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from linkedin_api_v2 import LinkedInPoster


class CPPQAPoster:
    """Automated C++ Q&A posting system for LinkedIn."""

    def __init__(self):
        """Initialize Q&A poster."""
        # Paths
        self.app_dir = Path(__file__).parent.parent
        self.qa_data_dir = self.app_dir / "data" / "data"
        self.tracker_file = self.app_dir / "tracker" / "qa_tracker.txt"
        self.history_file = self.app_dir / "logs" / "qa_history.json"

        self.logger = self._setup_logging()
        self.poster = LinkedInPoster()

    def _setup_logging(self):
        """Setup logging."""
        log_file = self.app_dir / "logs" / "qa_posting.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def _get_jst_now(self) -> datetime:
        """Get current datetime in JST timezone."""
        jst = timezone(timedelta(hours=9))
        return datetime.now(timezone.utc).astimezone(jst)

    def get_next_qa_post(self) -> Optional[Dict]:
        """
        Find next Q&A post from tracker.

        Returns:
            Dict with post_num, content_path, question_image_path, etc.
        """
        try:
            if not self.tracker_file.exists():
                self.logger.error(f"Tracker file not found: {self.tracker_file}")
                return None

            with open(self.tracker_file, 'r') as f:
                for line in f:
                    if line.strip().startswith('[ ]'):
                        # Parse: [ ] Post 1 | Virtual Destructor Bug
                        parts = line.strip().split('|')
                        if len(parts) >= 2:
                            post_part = parts[0].replace('[ ]', '').replace('Post', '').strip()
                            topic_title = parts[1].strip()

                            post_num = int(post_part)
                            post_prefix = f"{post_num:02d}"

                            return {
                                'post_num': post_num,
                                'content_path': self.qa_data_dir / f"{post_prefix}_content.txt",
                                'question_image_path': self.qa_data_dir / f"{post_prefix}_question_image.png",
                                'answer_path': self.qa_data_dir / f"{post_prefix}_answer.txt",
                                'answer_image_path': self.qa_data_dir / f"{post_prefix}_answer_image.png",
                                'topic': topic_title
                            }

            return None  # All posts complete

        except Exception as e:
            self.logger.error(f"Error reading tracker: {e}")
            return None

    def load_text_file(self, file_path: Path) -> str:
        """Load text from file."""
        with open(file_path, 'r') as f:
            return f.read().strip()

    def post_question(self, dry_run: bool = False) -> bool:
        """
        Post next C++ Q&A question.
        Marks as complete immediately - answers handled manually.

        Args:
            dry_run: If True, don't actually post

        Returns:
            True if successful
        """
        next_qa = self.get_next_qa_post()

        if next_qa is None:
            self.logger.info("🎉 All Q&A posts complete!")
            return True

        post_num = next_qa['post_num']
        content_path = next_qa['content_path']
        question_image_path = next_qa['question_image_path']
        topic = next_qa['topic']

        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"📅 C++ Q&A Post {post_num}: {topic}")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"📄 Content: {content_path.name}")
        self.logger.info(f"🖼️  Question Image: {question_image_path.name}")

        # Validate files
        if not content_path.exists():
            self.logger.error(f"❌ Content file not found: {content_path}")
            return False

        if not question_image_path.exists():
            self.logger.error(f"❌ Question image not found: {question_image_path}")
            return False

        # Load content
        caption = self.load_text_file(content_path)
        self.logger.info(f"📝 Caption length: {len(caption)} chars")

        if dry_run:
            self.logger.info("\n🔍 DRY RUN - Not actually posting")
            self.logger.info(f"Would post:\n{caption[:200]}...")
            return True

        # Post to LinkedIn
        self.logger.info("\n📤 Posting question to LinkedIn...")

        try:
            post_urn = self.poster.post_image(
                image_path=str(question_image_path),
                caption=caption
            )

            if post_urn:
                self.logger.info(f"\n✅ Question posted successfully!")
                self.logger.info(f"   Post URN: {post_urn}")

                # Mark as complete in tracker ([ ] → [X])
                self.mark_posted(post_num)

                # Log success
                self._log_event(post_num, 'question_posted', success=True, post_urn=post_urn, topic=topic)

                self.logger.info(f"   📝 Answer will be added manually via LinkedIn")
                return True
            else:
                self.logger.error(f"\n❌ Failed to post question for Post {post_num}")
                self._log_event(post_num, 'question_posted', success=False, topic=topic)
                return False

        except Exception as e:
            self.logger.error(f"\n❌ Posting error: {e}")
            self._log_event(post_num, 'question_posted', success=False, error=str(e), topic=topic)
            return False

    def mark_posted(self, post_num: int):
        """Mark post as complete in tracker ([ ] → [X])."""
        try:
            with open(self.tracker_file, 'r') as f:
                lines = f.readlines()

            updated = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f'[ ] Post {post_num} '):
                    lines[i] = line.replace('[ ]', '[X]', 1)
                    updated = True
                    break

            if updated:
                with open(self.tracker_file, 'w') as f:
                    f.writelines(lines)
                self.logger.info(f"✓ Marked Post {post_num} as [X] (complete)")

        except Exception as e:
            self.logger.error(f"Error updating tracker: {e}")

    def _log_event(self, post_num: int, event_type: str, success: bool, error: str = None, post_urn: str = None, topic: str = None):
        """Log Q&A posting event."""
        now_utc = datetime.now(timezone.utc)
        now_jst = self._get_jst_now()

        log_entry = {
            'timestamp': now_utc.isoformat(),
            'calendar_date_jst': now_jst.strftime('%Y-%m-%d'),
            'post_number': post_num,
            'topic': topic,
            'event_type': event_type,
            'success': success,
            'error': error,
            'post_urn': post_urn
        }

        # Append to history
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []

            history.append(log_entry)

            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            self.logger.warning(f"Could not write to history log: {e}")


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="LinkedIn C++ Q&A Auto Poster - Posts questions daily, answers handled manually",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection
  python3 qa_poster.py --test-connection

  # Post next question (dry run)
  python3 qa_poster.py --post-question --dry-run

  # Post next question (real)
  python3 qa_poster.py --post-question
        """
    )
    parser.add_argument("--dry-run", action="store_true", help="Test without actually posting")
    parser.add_argument("--test-connection", action="store_true", help="Test LinkedIn API connection")
    parser.add_argument("--post-question", action="store_true", help="Post next question (marks as complete)")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("LinkedIn C++ Q&A Auto Poster")
    print("="*60 + "\n")

    try:
        poster = CPPQAPoster()

        if args.test_connection:
            print("🔍 Testing LinkedIn API connection...")
            if poster.poster.test_connection():
                print("✅ Connection successful! Ready to post.")
                sys.exit(0)
            else:
                print("❌ Connection failed. Check credentials in config/.env")
                sys.exit(1)

        if args.post_question:
            success = poster.post_question(dry_run=args.dry_run)
            sys.exit(0 if success else 1)

        # No action specified
        parser.print_help()

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nSetup required:")
        print("1. Create config/.env file with LinkedIn credentials")
        print("2. See README.md for setup instructions")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
