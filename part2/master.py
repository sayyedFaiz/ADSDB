import subprocess
import sys
sys.path.append('./')


def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Successfully run {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_path}: {e}", file=sys.stderr)


def main():
    scripts_to_run = [
        'analyticalSandbox/analytical_sandboxes.py',
        'featureGeneration/featureGeneration/featuregeneration.py',
        'featureGeneration/dataPreparation/datapreparation.py',
        'featureGeneration/datalabelling/labeling.py',
        'trainingAndValidation/trainingAndTesting/machine_learning.py',
        # 'advanceTopic/featureSelection/pca.py',
        # 'advanceTopic/featureSelection/machine_learning.py',
    ]

    for script in scripts_to_run:
        print("Running..", script)
        run_script(script)
        print("\n*********************************************")


if __name__ == "__main__":
    main()
