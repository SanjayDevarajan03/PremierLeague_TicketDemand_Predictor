from pathlib import Path
import os

PARENT_DIR = Path(__file__).parent.resolve().parent
DATA_DIR = PARENT_DIR/'data'
RAW_DATA_weather_DIR = PARENT_DIR/'data'/'raw'/'weather_raw_data'
TRANSFORMED_DATA_DIR = PARENT_DIR/'data'/'transformed'
DATA_CACHE_DIR = PARENT_DIR/'data'/'cache'

MODELS_DIR = PARENT_DIR/'models'
Encoder_DIR = PARENT_DIR/'encoder'

def make_fundamental_paths() -> None:
    for path in [DATA_DIR, RAW_DATA_weather_DIR, 
                 TRANSFORMED_DATA_DIR, DATA_CACHE_DIR]:
        if not Path(path).exists():
            os.mkdir(path)


if __name__ == "__main__":
    os.chdir(PARENT_DIR)
    print(PARENT_DIR)