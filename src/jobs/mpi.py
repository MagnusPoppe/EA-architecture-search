import pickle
from mpi4py.futures import MPIPoolExecutor
from src.training import prepare_training as trainer


def pack_args(population, config):
    server_job_args = []
    config_str = pickle.dumps(config)
    epochs = config.training.epochs if config.training.fixed_epochs else 20
    for i, individ in enumerate(population):
        server_id = i % len(config.servers)
        server_job_args += [(
            pickle.dumps(population[i]),
            config_str,
            epochs,
            server_id,
            0,
            i
        )]
    return server_job_args


def launch_with_MPI_futures(population, config, tries=0):
    for individ in population:
        individ.failed = False

    args = pack_args(population, config)
    try:
        print(f"--> Starting MPI Pool executor. {len(args)} jobs running on {len(config.servers)} servers")
        with MPIPoolExecutor() as executor:
            results = [result for result in executor.map(trainer.run, args)]
            executor.shutdown(wait=True)
    except TypeError as e:
        print("Caught the infamous _thread.RLock exception")
        print(e)
        if tries > 0:
            exit(0)
        return launch_with_MPI_futures(population, config, tries=tries+1)

    # Exceptions may occur inside the async training loop.
    # The failed solutions will be discarded:
    original = len(results)
    results = [individ for individ in results if not individ.failed]
    filtered = len(results)
    print(f"--> Entire population trained. {original-filtered}/{original} failed.")
    for individ in results:
        del individ.failed

    return results
