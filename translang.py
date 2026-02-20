import runpy
import os

# Shim to allow running Streamlit from the repo root with:
#   streamlit run translang.py
# This executes the real app located at ProjectFiles/translang.py
here = os.path.dirname(__file__)
target = os.path.join(here, "ProjectFiles", "translang.py")
if not os.path.exists(target):
    raise FileNotFoundError(f"Expected app at {target!r}. If you moved files, update this shim or run Streamlit with the correct path.")

runpy.run_path(target, run_name="__main__")
