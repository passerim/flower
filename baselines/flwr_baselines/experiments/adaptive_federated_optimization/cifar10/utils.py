from pathlib import Path

import numpy as np
from click import Parameter
from flwr.common.parameter import weights_to_parameters
from flwr.common.typing import Parameters
from flwr.dataset.utils.common import XY, create_lda_partitions
from torch import save
from torch.nn import Module


def torch_model_to_parameters(model: Module) -> Parameters:
    weights = [val.cpu().numpy() for _, val in model.state_dict().items()]
    parameters = weights_to_parameters(weights)

    return parameters


def partition_and_save(
    dataset: XY,
    fed_dir: Path,
    dirichlet_dist: np.ndarray = None,
    num_partitions: int = 500,
    concentration: float = 0.1,
) -> np.ndarray:
    # Create partitions
    clients_partitions, dist = create_lda_partitions(
        dataset=dataset,
        dirichlet_dist=dirichlet_dist,
        num_partitions=num_partitions,
        concentration=concentration,
    )
    # Save partions
    for idx, partition in enumerate(clients_partitions):
        path_dir = fed_dir / f"{idx}"
        path_dir.mkdir(exist_ok=True, parents=True)
        save(partition, path_dir / "train.pt")

    return dist