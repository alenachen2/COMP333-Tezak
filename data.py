import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv = pd.read_csv("tezak2.csv")
# true_counts = df["count"].values
# cellpose_counts = df["CELLPOSE"].values
# tezak_model_counts = df["TEZAK"].values

# abs_error_cellpose = np.abs(true_counts - cellpose_counts).mean()
# print(abs_error_cellpose)

df = pd.DataFrame({
    "true_counts": csv["count"].values,
    "cellpose_counts": csv["CELLPOSE"].values,
    "tezak_model_counts": csv["TEZAK"].values
})

df = df.dropna()


#ABSOLUTE ERROR CALCULATION
df["abs_error_CPSAM"] = np.abs(df["true_counts"] - df["cellpose_counts"])
df["abs_error_TEZAK"] = np.abs(df["true_counts"] - df["tezak_model_counts"])

print("\nMean Abs Error with CPSAM:", df["abs_error_CPSAM"].mean())
print("\nMean Abs Error with TEZAK model:", df["abs_error_TEZAK"].mean())


#PERCENT ERROR CALCULATION
df["percent_error_CPSAM"] = 100 * df["abs_error_CPSAM"] / df["true_counts"]
df["percent_error_TEZAK"] = 100 * df["abs_error_TEZAK"] / df["true_counts"]

print("Mean Percent Error with CPSAM:", df["percent_error_CPSAM"].mean())
print("Mean Percent Error with TEZAK model:", df["percent_error_TEZAK"].mean())


#BIAS CALCULATION (does program over (+) or undercount (-))
df["bias_CPSAM"] = df["cellpose_counts"] - df["true_counts"]
df["bias_TEZAK"] = df["tezak_model_counts"] - df["true_counts"]

print("Mean Bias (signed error with CPSAM:)", df["bias_CPSAM"].mean())
print("Mean Bias (signed error with TEZAK model:)", df["bias_TEZAK"].mean())

over_avg_cpsam = df[df["bias_CPSAM"] > 0]["bias_CPSAM"].mean()
under_avg_cpsam = df[df["bias_CPSAM"] < 0]["bias_CPSAM"].mean()

over_avg_tezak = df[df["bias_TEZAK"] > 0]["bias_TEZAK"].mean()
under_avg_tezak = df[df["bias_TEZAK"] < 0]["bias_TEZAK"].mean()

print("Average CPSAM overcount:", over_avg_cpsam)
print("Average CPSAM undercount:", under_avg_cpsam)

print("Average TEZAK overcount:", over_avg_tezak)
print("Average TEZAK undercount:", under_avg_tezak)



#print(df)
#BLAND ALTMAN ANALYSIS

def bland_altman_plot(true, predicted, title):
    """
    Generates a Bland–Altman plot comparing true counts vs predicted counts.
    """
    means = (true + predicted) / 2
    diffs = predicted - true
    mean_diff = np.mean(diffs)
    sd_diff = np.std(diffs)

    plt.figure(figsize=(7, 5))
    plt.scatter(means, diffs)
    plt.axhline(mean_diff, color="red", linestyle="--", label=f"Mean diff = {mean_diff:.2f}")
    plt.axhline(mean_diff + 1.96 * sd_diff, color="gray", linestyle=":", label="+1.96 SD")
    plt.axhline(mean_diff - 1.96 * sd_diff, color="gray", linestyle=":", label="-1.96 SD")
    
    plt.title(title)
    plt.xlabel("Mean of True and Predicted Counts")
    plt.ylabel("Difference (Predicted – True)")
    plt.grid(True)
    plt.legend()
    plt.show()


bland_altman_plot(
    df["true_counts"].values,
    df["cellpose_counts"].values,
    "Bland–Altman: CPSAM vs True Counts"
)

bland_altman_plot(
    df["true_counts"].values,
    df["tezak_model_counts"].values,
    "Bland–Altman: TEZAK Model vs True Counts"
)