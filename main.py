import sys
from clarity.manager import WorkflowManager

if __name__ == "__main__":
    filename = sys.argv[1]
    pm = WorkflowManager.default()

    pm.run(filename)
