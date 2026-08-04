import logging
import subprocess

logger = logging.getLogger(__name__)


def launch_windows_app(*args: str) -> bool:
    """Launch a Windows application without a shell. Returns True on success."""
    try:
        subprocess.Popen(list(args))
        return True
    except Exception as e:
        logger.error("Failed to launch %s: %s", " ".join(args), e)
        return False
