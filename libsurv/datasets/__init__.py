import pandas as pd

from .data_simulator import SimulatedData
from .base import survival_statistics
from .base import survival_df
from .base import survival_dmat

__ALL__ = [
    "survival_statistics",
    "survival_df",
    "survival_dmat",
    "load_simulated_data",
    "load_metabric",
    "load_metabric_train",
    "load_metabric_test",
    "load_whas",
    "load_whas_train",
    "load_whas_test",
    "SimulatedData"
]

def _load_dataset(filename, **kwargs):
    """
    Load a dataset from libsurv.datasets

    Parameters
    ----------
    filename : string
        for example "whas_train.csv"
    usecols : list
        list of columns in file to use

    Returns
    -------
        output: DataFrame
    """
    return pd.read_csv(resource_filename("libsurv", "datasets/src/" + filename), engine="python", **kwargs)

def load_metabric_train(**kwargs):
    """
    Load a training dataset of METABRIC

    Notes
    -----
    See `load_metabric` for more details.
    """
    return _load_dataset("metabric_train.csv", **kwargs)

def load_metabric_test(**kwargs):
    """
    Load a test dataset of METABRIC

    Notes
    -----
    See `load_metabric` for more details.
    """
    return _load_dataset("metabric_test.csv", **kwargs)

def load_metabric(**kwargs):
    """
    Load a dataset of METABRIC.

    Notes
    -----
    The Molecular Taxonomy of Breast Cancer International Consortium (METABRIC) investigates 
    the effect of gene and protein expression profiles on breast cancer survival, and help 
    physicians design better treatment recommendations. Statistics are below:

    # Rows: 1903
    # Columns: 9 + Event + Time
    # Event Ratio: 57.96%
    # Min Time: 1 (months)
    # Max Time: 356 (months)

    """
    data_train = load_metabric_train(**kwargs)
    data_test = load_metabric_test(**kwargs)
    # merge into a dataframe
    data = pd.concat([d_train, d_test], axis=0)
    return data.reset_index(drop=True)

def load_whas_train(**kwargs):
    """
    Load a training dataset of WHAS

    Notes
    -----
    See `load_whas` for more details.
    """
    return _load_dataset("whas_train.csv", **kwargs)

def load_whas_test(**kwargs):
    """
    Load a test dataset of WHAS

    Notes
    -----
    See `load_whas` for more details.
    """
    return _load_dataset("whas_test.csv", **kwargs)

def load_whas(**kwargs):
    """
    Load a dataset of WHAS.

    Notes
    -----
    WHAS(the Worcester Heart Attack Study (WHAS) [18] studies the survival of acute myocardial 
    infraction (MI). Statistics are below:

    # Rows: 1638
    # Columns: 5 + Event + Time
    # Event Ratio: 42.12%
    # Min Time: 1 (months)
    # Max Time: 67 (months)

    """
    data_train = load_whas_train(**kwargs)
    data_test = load_whas_test(**kwargs)
    # merge into a dataframe
    data = pd.concat([d_train, d_test], axis=0)
    return data.reset_index(drop=True)

def load_simulated_data(hr_ratio,
        N=1000, num_features=10, num_var=2,
        average_death=5, end_time=15,
        method="gaussian",
        gaussian_config={},
        seed=42):
    """
    Load simulated data generated by the exponentional distribution.

    Parameters
    ----------
    hr_ratio: int or float
        `lambda_max` hazard ratio.
    N: int
        The number of observations.
    average_death: int or float
        Average death time that is the mean of the Exponentional distribution.
    end_time: int or float
        Censoring time that represents an 'end of study'. Any death 
        time greater than end_time will be censored.
    num_features: int
        Size of observation vector. Default: 10.
    num_var: int
        Number of varaibles simulated data depends on. Default: 2.
    method: string
        The type of simulated data. 'linear' or 'gaussian'.
    gaussian_config: dict
        Dictionary of additional parameters for gaussian simulation.
    seed: int
        Random state.

    Returns
    -------
    pandas.DataFrame
        A simulated survival dataset following the given args.

    Notes
    -----
    Peter C Austin. Generating survival times to simulate cox proportional
    hazards models with time-varying covariates. Statistics in medicine,
    31(29):3946-3958, 2012.
    """
    generator = SimulatedData(hr_ratio, average_death=average_death, end_time=end_time, 
                              num_features=num_features, num_var=num_var)
    raw_data = generator.generate_data(N, method=method, gaussian_config=gaussian_config, seed=seed)
    # To DataFrame
    df = pd.DataFrame(raw_data['x'], columns=['x_' + str(i) for i in range(num_features)])
    df['e'] = raw_data['e']
    df['t'] = raw_data['t']
    return df
