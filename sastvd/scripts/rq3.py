import sastvd as svd
import sastvd.linevd.run as lvdrun
from ray import tune

config = {
    "hfeat": tune.choice([512]),
    "embtype": tune.choice(["codebert"]),
    "stmtweight": tune.choice([1, 5, 10]),
    "hdropout": tune.choice([0.25, 0.3]),
    "gatdropout": tune.choice([0.15, 0.2]),
    "modeltype": tune.choice(["gat1layer"]),
    "gnntype": tune.choice(["gat"]),
    "loss": tune.choice(["ce"]),
    "scea": tune.choice([0.4, 0.5, 0.6]),
    "gtype": tune.choice(["pdg"]),
    "batch_size": tune.choice([1024]),
    "multitask": tune.choice(["line", "linemethod"]),
    "splits": tune.choice(["default"]),
}

samplesz = -1
run_id = svd.get_run_id()
sp = svd.get_dir(svd.processed_dir() / f"raytune_method_{samplesz}" / run_id)
trainable = tune.with_parameters(lvdrun.train_linevd, samplesz=samplesz, savepath=sp)

analysis = tune.run(
    trainable,
    resources_per_trial={"cpu": 1, "gpu": 1},
    metric="val_loss",
    mode="min",
    config=config,
    num_samples=1000,
    name="tune_linevd",
    local_dir=sp,
    keep_checkpoints_num=2,
    checkpoint_score_attr="min-val_loss",
)