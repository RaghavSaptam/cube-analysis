import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("full_cube.csv")


def to_seconds(t):
    if ":" in t:
        m,s = t.split(":")
        return int(m)*60 + float(s)
    else:
        return float(t)

df["seconds"] = df["time"].apply(to_seconds)


df["prev_time"] = df["seconds"].shift(1)
df["rolling_mean_5"] = df["seconds"].rolling(5).mean()
df["rolling_std_5"] = df["seconds"].rolling(5).std()


df["move_count"] = df["scramble"].apply(lambda x: len(x.split()))
df["prime_moves"] = df["scramble"].apply(lambda x: x.count("'"))
df["double_moves"] = df["scramble"].apply(lambda x: x.count("2"))


mean = df["seconds"].mean()
std = df["seconds"].std()

df["slow_solve"] = df["seconds"] > mean + std


print("Average:", df["seconds"].mean())
print("Best:", df["seconds"].min())
print("Worst:", df["seconds"].max())
print("Std Dev:", df["seconds"].std())
print("Slow solves:", df["slow_solve"].sum())



fig, axs = plt.subplots(3, 1, figsize=(6,10))

# trend
axs[0].plot(df["index"], df["seconds"])
axs[0].set_title("Solve Time Trend")

# histogram
axs[1].hist(df["seconds"], bins=15)
axs[1].set_title("Distribution")

# rolling mean
axs[2].plot(df["index"], df["rolling_mean_5"])
axs[2].set_title("Rolling Mean (5)")

plt.tight_layout()
plt.show()

