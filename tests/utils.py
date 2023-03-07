# pylint: disable=duplicate-code

import platform
import subprocess as sub

import numpy as np
import pandas as pd
import seaborn as sns


# ============================================
#                   clear
# ============================================
def clear() -> None:
    try:
        sub.run(
            ["cls" if "windows" == platform.system().lower() else "clear"], check=True
        )
    # For git bash
    except FileNotFoundError:
        sub.run(["clear"], check=True)


# ============================================
#                    plot
# ============================================
def plot(desired, measured, times, label, figName):
    nValues = len(times)
    t = np.concatenate((times, times))
    dataType = ["Desired"] * nValues + ["Measured"] * nValues
    data = np.concatenate((desired, measured))

    data = {
        "Time (ms)": t,
        "Type": dataType,
        label: data,
    }

    df = pd.DataFrame(data)

    plt = sns.relplot(data=df, x="Time (ms)", y=label, hue="Type", kind="line")

    plt.figure.savefig(figName)
