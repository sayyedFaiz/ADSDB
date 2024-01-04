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
        # 'analyticalSandbox/analytical_sandbox_profiling.py',
        'featureGeneration/featureGeneration/featuregeneration.py',
        'featureGeneration/dataPreparation/datapreparation.py',
        'featureGeneration/datalabelling/labeling.py',
        # 'featureGeneration/trainingAndValidationDatasets/training_testing_sets.py',
        # 'featureGeneration/trainingAndValidationDatasets/training_valitdation_profiling.py',
        'trainingAndValidation/trainingAndTesting/machine_learning.py',
        # 'trainingAndValidation/visualization/visualize_model_comparison.py'
        'advanceTopic/featureSelection/pca.py',
        # 'advanceTopic/featureSelection/machine_learning.py',
    ]

    for script in scripts_to_run:
        print("Running..", script)
        run_script(script)
        print("\n*********************************************")


if __name__ == "__main__":
    main()
