from pydub import AudioSegment


def is_silent(segment, threshold=-30):
    """
    Check if an audio segment contains silence based on a threshold
    """
    # 
    return segment.dBFS < threshold

def is_corrupted(file_path):
    """Check if an audio file is corrupted (you may need to customize this)
    """
    # 
    try:
        AudioSegment.from_file(file_path)
        return False
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return True