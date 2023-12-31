import sys
import subprocess
sys.path.append('./')


def main():
    income = float(sys.argv[1])
    district1 = sys.argv[2]
    district2 = sys.argv[3]
    year = int(sys.argv[4])
    test = sys.argv[5]
    command = [
        "python",
        "featureGeneration/featureGeneration/featuregeneration.py",
        str(income),
        district1,
        district2,
        str(year),
        test
    ]

    command2 = [
        "python",
        "featureGeneration/dataPreparation/datapreparation.py",
        test
    ]

    command3 = [
        "python",
        "trainingAndValidation/trainingAndTesting/machine_learning.py",
        test
    ]

    try:
        subprocess.run(command, check=True)
        subprocess.run(command2, check=True)
        subprocess.run(command3, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running .py file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
